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

## Core Design Principles

**These are immutable contracts that must be upheld in every contribution to prevent regressions.**

### 1. Visualization Contract

> **`visualize_result(gmap, result)` must only animate the return value of the user's own `solve()`. Never run a reference algorithm inside this function.**

If a reference algorithm (e.g. `bfs_sim`) runs inside `visualize_result`, users see a correct path animation even when their code is incomplete or wrong. This gives a false sense of success and destroys the educational value of the tool.

Correct behaviour:
- `solve()` returns empty (`[]`, `None`, `{}`) → `visualize_result()` returns `None` → base map shown with "Incomplete" status, no animation
- `solve()` returns a valid path → animate **only** that path, cell by cell

```python
# WRONG — ignores result, runs reference BFS regardless of user code
def visualize_result(gmap, result):
    from core import bfs_sim
    return bfs_sim(gmap, start, goal)   # always shows the correct path

# CORRECT — only visualize what the user's solve() returned
def visualize_result(gmap, result):
    if not result:
        return None   # incomplete → no animation
    # animate result (list of (r,c) cells) step by step
```

Affected files: every `visualize_result()` in `engines/mission_XX.py`.

### 2. Completion Contract

> `watcher.py` only marks a mission complete when the file's `mtime` has changed since watcher startup. The initial auto-trigger on startup never counts as a completion.

Implementation: record `startup_mtime = os.path.getmtime(solution_path)` at startup; call `mark_complete()` only when `os.path.getmtime(changed_path) > startup_mtime`.

This prevents pre-existing `saves/` files (with working code from a previous session) from auto-completing a mission the moment the user opens the code window.

### 3. Editor File Contract

> Files in `saves/` are the user's working copies. Files in `problems/` are read-only templates.

- `saves/XX.py` — edited by the user, watched by `watcher.py`
- `problems/XX.py` — template only; never modified directly (copied to `saves/` on first launch)

---

## Agent Workflow

**Every agent must read the "Core Design Principles" section above before starting any task.** When modifying `engines/` or `watcher.py`, explicitly verify that the changes do not violate the Visualization Contract or the Completion Contract.

Use the Task tool's sub-agents to maintain consistency across the codebase.

### Agent Roles by Situation

| Situation | Required Agent | Reason |
|-----------|---------------|--------|
| Bulk scan or edit of `problems/` | `Explore` | Parallel traversal of 43 files and their headers |
| Impact analysis before changing `engines/` | `Explore` | Map engine-to-problem file dependencies |
| Architecture change in `warfront/` package | `Plan` | Design interface changes before touching shared modules |
| Bulk creation of new missions or problem files | `general-purpose` | Parallel generation keeps files consistent |
| Bug with unclear root cause | `Explore` | Trace the watcher → sandbox → engine execution chain |

### Rules

1. **Modifying 2+ files in `problems/`** → use an `Explore` agent first to identify all affected files before making changes.
2. **Modifying `engines/mission_XX.py`** → use an `Explore` agent to confirm which `problems/` files reference that engine.
3. **Changing a shared module in `warfront/`** (`config`, `data/models`, `data/progress`) → use a `Plan` agent to review the design before implementing.
4. **Adding a new feature** (new algorithm mission, new rank tier, etc.) → `Plan` agent for design, then `general-purpose` agent for implementation.
5. **Single-file fix or small bug** → no agent needed, work directly.

### Example

```python
# Bad — grep problems/ directly, floods context window
Grep("MODULE:", "problems/")

# Good — delegate to Explore agent
Task(subagent_type="Explore", prompt="List all files in problems/ where MODULE: is 'none', and show each file's full header block.")
```
