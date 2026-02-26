#!/usr/bin/env bash
# WARFRONT Start Script
# Usage:
#   bash start.sh              → Run in saved mode (select if not found)
#   bash start.sh --mode terminal
#   bash start.sh --mode browser

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON=$(which python3 || which python)
SESSION="warfront"
MODE_FILE="$HOME/.warfront_mode"

# ── Argument Parsing ─────────────────────────────────────────
FORCE_MODE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode) FORCE_MODE="$2"; shift 2 ;;
        -m)     FORCE_MODE="$2"; shift 2 ;;
        terminal|browser) FORCE_MODE="$1"; shift ;;
        *) shift ;;
    esac
done

# ── Banner ──────────────────────────────────────────────────
clear
cat << 'BANNER'

  ██╗    ██╗ █████╗ ██████╗ ███████╗███████╗██████╗  ██████╗ ███╗   ██╗████████╗
  ██║    ██║██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
  ██║ █╗ ██║███████║██████╔╝█████╗  █████╗  ██████╔╝██║   ██║██╔██╗ ██║   ██║
  ██║███╗██║██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║   ██║
  ╚███╔███╔╝██║  ██║██║  ██║██║     ██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║
   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝

BANNER

# ── Mode Selection ───────────────────────────────────────────
if [ -n "$FORCE_MODE" ]; then
    # Forced by --mode argument
    case "$FORCE_MODE" in
        terminal|1) MODE="terminal" ;;
        browser|2)  MODE="browser"  ;;
        *)
            echo "  ❌  Unknown mode: $FORCE_MODE"
            echo "  Usage: bash start.sh --mode terminal"
            echo "         bash start.sh --mode browser"
            exit 1
            ;;
    esac
    echo "$MODE" > "$MODE_FILE"
    echo "  Mode changed to: $MODE"
    sleep 0.5

elif [ -f "$MODE_FILE" ]; then
    # Auto-load saved mode
    MODE=$(cat "$MODE_FILE")
    if [ "$MODE" != "terminal" ] && [ "$MODE" != "browser" ]; then
        MODE="terminal"
    fi
    if   [ "$MODE" = "terminal" ]; then LABEL="🖥️  Terminal Mode  (vi editor)"
    else                                LABEL="🌐  Browser Mode (web editor)"; fi
    echo "  Saved Mode: $LABEL"
    echo "  To change: bash start.sh --mode terminal  OR  --mode browser"
    echo ""

else
    # First run: Selection UI
    echo "  Select coding editor mode"
    echo ""
    echo "  [1]  🖥️  Terminal Mode   —  tmux + vi editor"
    echo "  [2]  🌐  Browser Mode    —  web editor (localhost:7477)"
    echo ""
    echo -n "  Choice (1 or 2, default 1): "
    read -r CHOICE
    case "${CHOICE:-1}" in
        2|browser)  MODE="browser"  ;;
        *)          MODE="terminal" ;;
    esac
    echo "$MODE" > "$MODE_FILE"
    echo ""
    if   [ "$MODE" = "terminal" ]; then echo "  ✅  Terminal Mode selected — Saved"
    else                                echo "  ✅  Browser Mode selected — Saved"; fi
    sleep 0.8
fi

# ── Flask Check (Browser Mode) ──────────────────────────────
if [ "$MODE" = "browser" ]; then
    if ! $PYTHON -c "import flask" 2>/dev/null; then
        echo ""
        echo "  ⚠️   Flask not installed — Required for Browser Mode"
        echo -n "  Install now? (y/n, default y): "
        read -r yn
        case "${yn:-y}" in
            y|Y|"") pip install flask -q && echo "  ✅  Flask installed" ;;
            *)      echo "  ❌  Cannot run Browser Mode without Flask"; exit 1 ;;
        esac
    fi
fi

# ── Start tmux Session ───────────────────────────────────────
if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux kill-session -t "$SESSION"
    sleep 0.3
fi

tmux new-session -d -s "$SESSION" -n "MENU"
sleep 0.3

# Pass WARFRONT_MODE environment variable to main.py
tmux send-keys -t "${SESSION}:MENU" \
    "cd '$BASE_DIR' && WARFRONT_MODE=$MODE $PYTHON '$BASE_DIR/main.py'" Enter

tmux attach-session -t "$SESSION"
