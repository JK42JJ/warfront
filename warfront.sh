#!/usr/bin/env bash
# WARFRONT v2.0 Launcher — 3-pane tmux layout (drops header.py pane)
MISSION=${1:-01}
PROBLEM_FILE=${2:-}
MODULE=${3:-none}
RANK_NAME=${4:-Private}
BAR_BG=${5:-colour58}
BAR_FG=${6:-colour226}
ALREADY_DONE=${7:-0}

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION="warfront"
PYTHON=$(which python3 || which python)
SAVES_DIR="$BASE_DIR/saves"
SAVE_FILE="$SAVES_DIR/$(basename "$PROBLEM_FILE")"
[ ! -f "$SAVE_FILE" ] && cp "$PROBLEM_FILE" "$SAVE_FILE"

# 1. Kill existing CODE window and create fresh one
tmux kill-window -t "${SESSION}:CODE" 2>/dev/null
tmux new-window -t "$SESSION" -n "CODE"

# 2. 3-pane layout:
#    Pane 0 (top-left,  ~70%): editor (vim)
#    Pane 1 (top-right, ~30%): watcher / visualization
#    Pane 2 (bottom,    ~25%): error log (io_watcher)
tmux split-window -h -t "${SESSION}:CODE"    -p 40
tmux split-window -v -t "${SESSION}:CODE.1"  -p 35

# 3. Vim config
VIMRC="$BASE_DIR/.vimrc_warfront"
cat <<'VIMEOF' > "$VIMRC"
set nocompatible
set termguicolors
syntax on
set number
set cursorline
set tabstop=4
set shiftwidth=4
set expandtab
hi Normal      guibg=#161b22 guifg=#c9d1d9
hi NonText     guibg=#161b22 guifg=#161b22
hi EndOfBuffer guibg=#161b22 guifg=#161b22
hi LineNr      guibg=#161b22 guifg=#484f58
hi SignColumn  guibg=#161b22
hi CursorLine  guibg=#21262d
hi Statement   guifg=#ff7b72
hi Keyword     guifg=#ff7b72
hi Function    guifg=#d2a8ff
hi String      guifg=#a5d6ff
hi Comment     guifg=#8b949e
VIMEOF

# 4. Start each pane
# Editor (pane 0)
tmux send-keys -t "${SESSION}:CODE.0" "vim -u '$VIMRC' '$SAVE_FILE'" Enter

# Watcher / visualization (pane 1)
tmux send-keys -t "${SESSION}:CODE.1" \
    "cd '$BASE_DIR' && clear && $PYTHON watcher.py '$MISSION' '$SAVE_FILE' '$MODULE' '$ALREADY_DONE'" Enter

# Error log (pane 2)
tmux send-keys -t "${SESSION}:CODE.2" \
    "cd '$BASE_DIR' && clear && $PYTHON io_watcher.py '.warfront_log' '$SAVE_FILE'" Enter

# 5. Focus editor
tmux select-pane -t "${SESSION}:CODE.0"
tmux set-option -t "$SESSION" status-style "bg=${BAR_BG},fg=${BAR_FG}"
tmux select-window -t "${SESSION}:CODE"
