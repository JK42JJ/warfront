# ⚔ WARFRONT — Algorithm Tactical Simulator

WARFRONT is a Python-based CLI algorithm tactical simulator designed to help developers master core algorithms (BFS, Dijkstra, MST, etc.) through tactical warfare-themed scenarios. It features a progress-tracking rank system and real-time execution visualization.

## 🚀 Project Overview

- **Main Technologies:** Python 3.9+, [Rich](https://github.com/Textualize/rich) (CLI visualization), `tmux` (terminal management).
- **Core Concept:** "Tactical Situations" mapped to algorithms:
    - BFS → Escape from encirclement (Shortest path).
    - Dijkstra → Drone reconnaissance (Varying terrain costs).
    - Topological Sort → Mission planning (Dependencies).
- **Key Components:**
    - `main.py`: Entry point, mission selector, and progress tracker.
    - `core.py`: Pure algorithm implementations using a **Step Snapshot System**.
    - `map.py`: Simulation environment (Grid, Terrains, Units).
    - `renderer.py`: Visual engine using Rich for terminal rendering.
    - `watcher.py`: File watcher that re-runs simulations on `solution.py` save.

## 🛠 Installation & Setup

### 🍎 macOS (Recommended)
1. **Prerequisites**: Install Homebrew and Python 3.9+.
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python tmux
   ```
2. **Setup**:
   ```bash
   git clone https://github.com/yourusername/warfront.git
   cd warfront
   pip install -r requirements.txt
   ```
3. **Run**:
   ```bash
   python main.py
   ```

### 🪟 Windows
Windows users are recommended to use **WSL (Windows Subsystem for Linux)** for the best experience, as `tmux` and `termios` are Unix-native.

1. **Prerequisites**: Install WSL (Ubuntu is recommended).
   - Open PowerShell as Admin and run: `wsl --install`
   - Restart your computer if prompted.
2. **In WSL (Ubuntu Terminal)**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip tmux
   ```
3. **Setup**:
   ```bash
   git clone https://github.com/yourusername/warfront.git
   cd warfront
   pip3 install rich
   ```
4. **Run**:
   ```bash
   python3 main.py
   ```

*Note: Native Windows execution via CMD/PowerShell is currently not supported due to `tmux` and `termios` dependencies.*

## 📐 Development Conventions

### ⚠️ Core Design Contract — Must Read Before Modifying Any Engine File

**Visualization Contract** (the most critical rule):

> `visualize_result(gmap, result)` must **only** visualize the user's `solve()` return value.
> **Never** call a reference algorithm (`bfs_sim`, `dijkstra_sim`, etc.) inside `visualize_result`.

Why this matters: if a reference algorithm runs inside `visualize_result`, users see a correct path animation even when their code is incomplete or wrong — making them falsely believe their implementation works. This destroys the educational value of the tool.

```python
# ❌ WRONG — reference algorithm ignores user's result (causes "false success" bug)
def visualize_result(gmap, result):
    return bfs_sim(gmap, start, goal)   # always shows the correct path

# ✅ CORRECT — only visualize what the user's code returned
def visualize_result(gmap, result):
    if not result:
        return None          # incomplete → no animation, shows "Incomplete" status
    # animate result (list of (r,c) cells) step by step
```

**Completion Contract**:

> `watcher.py` only signals mission complete when the file's `mtime` has changed since watcher startup.
> The initial auto-trigger on watcher start never counts as a completion.

This prevents pre-existing saves files (with working code from a previous session) from auto-completing a mission when the user opens the code window.

### Step Snapshot System
All algorithms in `core.py` must return a list of snapshots to be rendered sequentially.
- Format: `List[Tuple[State, Description, ExtraInfo]]`
- The `snapshot(gmap)` utility in `core.py` should be used to copy the map state for each step.

## 📝 Backlog & Roadmap
- [ ] **Plugin System**: Support for adding external "Code Sets" (Mission Packs) as plugins.
- [ ] **Native Windows Support**: Exploration of `Textual` or `Prompt_Toolkit` for cross-platform UI.
- [ ] **Online Leaderboard**: Global rank synchronization.

## 📄 License
This project is licensed under the MIT License.
