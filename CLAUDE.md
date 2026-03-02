# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the simulator
python main.py
# or
./start.sh                    # Interactive mode selection
./start.sh --mode terminal    # Force terminal mode (requires tmux)
./start.sh --mode browser     # Force browser mode (Flask on port 7477)

# Install dependencies
pip install rich              # Required
pip install flask             # Optional (browser mode only)
brew install tmux             # macOS, required for terminal mode
```

There is no test runner — testing is implicit via `watcher.py`, which monitors `solution.py` and re-executes the active mission's test scenarios on every save.

## Architecture

WARFRONT is a Python 3.9+ CLI educational tool. Users select missions from a menu, implement `solve()` in `solution.py`, save the file, and watch real-time algorithm visualization in tmux panes.

### Execution Flow

1. `start.sh` → `main.py` (mission menu, progress tracking)
2. Mission selection → `warfront.sh` (creates 4-pane tmux session)
3. User edits `solution.py` in editor pane
4. `watcher.py` detects file save → imports `solution.py`, runs `solve()` against mission test data
5. Results rendered via `renderer.py` in visualization pane
6. `io_watcher.py` tails `.warfront_log` for error display
7. Success signals written to `.warfront_done` → progress updated in `.warfront_progress.json`

### Core Components

| File | Responsibility |
|------|---------------|
| `map.py` | Data structures only: `GameMap`, `Cell`, `Terrain` enum, `UnitType` enum |
| `core.py` | Pure algorithm logic (no I/O): `bfs_sim()`, `dfs_sim()`, `dijkstra_sim()`, etc. |
| `renderer.py` | Rich-based terminal rendering only |
| `watcher.py` | Orchestration: file watch → execute → visualize |
| `engines/mission_XX.py` | Per-algorithm test scenarios (`build_map()`, `get_test_data()`) |
| `problems/` | 43 student-facing problem files |
| `ranks.py` | 40-rank progression system across 5 tiers |
| `config.py` | Singleton `cfg` with animation speeds, paths, UI settings |

### Step Snapshot System

All algorithms in `core.py` return `List[Tuple[State, Description, ExtraInfo]]`. Each step captures a deep-copied map state via `snapshot(gmap)`. The renderer iterates these snapshots to animate execution.

### Problem File Convention

Every file in `problems/` must include this header:
```python
# MISSION: <no> | <algo> | <level>
# TITLE: <title>
# DESC: <short description>
# MODULE: <associated_mission_module>
```

Naming format: `{number}_{algorithm}_{difficulty}.py` (e.g., `01_bfs_beginner.py`).

### IPC Signal Files

Runtime coordination uses sentinel files in the project root:
- `.warfront_done` — mission completed successfully
- `.warfront_attempt` — execution attempted
- `.warfront_log` — live error/output log
- `.warfront_progress.json` — persisted user progress and rank

## Core Design Principles (핵심 설계 원칙)

**이 섹션은 향후 작업 시 리그레션을 방지하기 위한 불변 원칙이다. 반드시 준수해야 한다.**

### 1. 시각화 계약 (Visualization Contract)

WARFRONT의 핵심 철학:
> **사용자가 작성한 `solve()`의 결과만 시각화한다. 절대로 참조 구현(reference algorithm)을 시각화에 사용하지 않는다.**

**올바른 동작**:
- `solve()` 반환값이 비어있음 (`[]`, `None`, `{}`) → `visualize_result()`는 `None` 반환 → 베이스 맵 + "Incomplete" 상태 표시
- `solve()` 반환값이 유효한 경로 → 사용자의 실제 경로만 애니메이션

**절대 금지 (regression 원인)**:
```python
# ❌ 틀린 구현 — 참조 알고리즘으로 시각화 (배신감 버그)
def visualize_result(gmap, result):
    from core import bfs_sim          # result를 무시하고 참조 BFS 실행
    return bfs_sim(gmap, start, goal) # 사용자 코드가 틀려도 "정답" 경로가 시각화됨

# ✅ 올바른 구현 — 사용자 결과만 시각화
def visualize_result(gmap, result):
    if not result:
        return None                   # 미완성이면 아무것도 표시 안 함
    # ... 사용자의 result로만 경로 표시
```

**영향받는 파일**: `engines/mission_XX.py`의 모든 `visualize_result()` 함수

### 2. 완료 처리 계약 (Completion Contract)

> **`watcher.py`는 사용자가 실제로 파일을 저장한 경우에만 완료 처리한다. 워처 시작 시 자동 트리거는 완료로 인정하지 않는다.**

구현: `watcher.py`에서 `startup_mtime`을 기록하고, `os.path.getmtime(changed_path) > startup_mtime`일 때만 `mark_complete()` 호출.

**절대 금지**: 워처 시작 시 초기 트리거(`file_queue.put(solution_path)`)로 완료 처리.

### 3. 에디터 파일 계약 (Editor File Contract)

> **`saves/` 디렉토리의 파일은 사용자의 작업본이다. 원본 `problems/` 파일은 읽기 전용 템플릿이다.**

- `saves/XX.py` ← 사용자가 편집, watcher가 감시
- `problems/XX.py` ← 템플릿, 직접 수정 금지 (init 시 saves에 복사됨)

---

## Agent Workflow (팀 에이전트 필수 지침)

**모든 에이전트는 작업 시작 전에 위의 "Core Design Principles" 섹션을 반드시 숙지해야 한다.**
특히 `engines/` 또는 `watcher.py`를 수정하는 경우, Visualization Contract와 Completion Contract를 위반하지 않도록 검토한다.

작업 일관성을 위해 아래 규칙에 따라 Task 툴의 서브에이전트를 **반드시** 활용한다.

### 역할별 에이전트 분리

| 상황 | 필수 에이전트 | 이유 |
|------|-------------|------|
| `problems/` 전체 스캔·일괄 수정 | `Explore` | 43개 파일의 헤더·구조를 병렬 탐색 |
| `engines/` 알고리즘 변경 전 영향 분석 | `Explore` | 엔진-문제 파일 의존 관계 파악 |
| `warfront/` 패키지 아키텍처 변경 | `Plan` | 모듈 간 인터페이스 변경의 파급 효과 설계 |
| 새 미션/문제 파일 일괄 생성 | `general-purpose` | 병렬 생성으로 파일 간 일관성 유지 |
| 버그 원인 불명확 시 | `Explore` | watcher·sandbox·engine 연쇄 흐름 추적 |

### 구체적 규칙

1. **`problems/` 2개 이상 파일 수정** → 먼저 `Explore` 에이전트로 영향받는 파일 전체 목록 확인 후 작업
2. **`engines/mission_XX.py` 수정** → `Explore` 에이전트로 해당 엔진을 참조하는 `problems/` 파일 확인 필수
3. **`warfront/` 패키지 내 공용 모듈(`config`, `data/models`, `data/progress`) 변경** → `Plan` 에이전트로 설계 검토 후 구현
4. **신규 기능(새 알고리즘 미션, 새 rank tier 등) 추가** → `Plan` 에이전트로 전체 설계 → `general-purpose` 에이전트로 구현 파이프라인 분리
5. **단순 1-파일 수정·버그 수정** → 에이전트 불필요, 직접 작업 가능

### 에이전트 사용 예시

```
# 나쁜 예: 에이전트 없이 problems/ 전체를 직접 grep
Grep("MODULE:", "problems/")  # 컨텍스트 낭비

# 좋은 예: Explore 에이전트에 위임
Task(subagent_type="Explore", prompt="problems/ 디렉토리에서 MODULE: none인 파일 목록과 각 파일의 헤더 정보를 수집해줘")
```
