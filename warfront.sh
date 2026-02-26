#!/usr/bin/env bash
# WARFRONT Launcher (Architectural Fix: Config-based)
MISSION=${1:-01}; PROBLEM_FILE=${2:-}; MODULE=${3:-none}
RANK_NAME=${4:-Private}; BAR_BG=${5:-colour58}; BAR_FG=${6:-colour226}
ALREADY_DONE=${7:-0}

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION="warfront"
PYTHON=$(which python3 || which python)
SAVES_DIR="$BASE_DIR/saves"
SAVE_FILE="$SAVES_DIR/$(basename "$PROBLEM_FILE")"
[ ! -f "$SAVE_FILE" ] && cp "$PROBLEM_FILE" "$SAVE_FILE"

# 1. Configure Window Layout
tmux kill-window -t "${SESSION}:CODE" 2>/dev/null
tmux new-window -t "$SESSION" -n "CODE"
tmux split-window -v -b -t "${SESSION}:CODE" -l 3
tmux split-window -h    -t "${SESSION}:CODE.1" -p 45
tmux split-window -v    -t "${SESSION}:CODE.2" -p 30

# 2. Create temporary Vim config file
VIMRC="$BASE_DIR/.vimrc_warfront"
cat <<EOF > "$VIMRC"
set nocompatible
set termguicolors
syntax on
set number
set cursorline
set tabstop=4
set shiftwidth=4
set expandtab
hi Normal guibg=#161b22 guifg=#c9d1d9
hi NonText guibg=#161b22 guifg=#161b22
hi EndOfBuffer guibg=#161b22 guifg=#161b22
hi LineNr guibg=#161b22 guifg=#484f58
hi SignColumn guibg=#161b22
hi CursorLine guibg=#21262d
hi Statement guifg=#ff7b72
hi Keyword guifg=#ff7b72
hi Function guifg=#d2a8ff
hi Symbol guifg=#d2a8ff
hi String guifg=#a5d6ff
hi Comment guifg=#8b949e
EOF

# 3. Execute each panel
tmux send-keys -t "${SESSION}:CODE.0" "cd '$BASE_DIR' && clear && $PYTHON header.py" Enter
tmux send-keys -t "${SESSION}:CODE.2" "cd '$BASE_DIR' && clear && $PYTHON watcher.py '$MISSION' '$SAVE_FILE' '$MODULE' '$ALREADY_DONE'" Enter
tmux send-keys -t "${SESSION}:CODE.3" "cd '$BASE_DIR' && clear && $PYTHON io_watcher.py '.warfront_log' '$SAVE_FILE'" Enter

# 4. Execute Editor
tmux send-keys -t "${SESSION}:CODE.1" "vim -u '$VIMRC' '$SAVE_FILE'" Enter

# 5. Force Focus
tmux select-pane -t "${SESSION}:CODE.1"
tmux set-option -t "$SESSION" status-style "bg=${BAR_BG},fg=${BAR_FG}"
tmux select-window -t "${SESSION}:CODE"
