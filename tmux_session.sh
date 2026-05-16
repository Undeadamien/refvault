#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")" || exit 0

NAME_SESSION="refvault"
PROJECT_DIR="$(pwd)"

if tmux has-session -t "$NAME_SESSION" 2>/dev/null; then
    tmux kill-session -t "$NAME_SESSION"
fi

if [ ! -f .venv/bin/activate ]; then python -m venv .venv; fi

tmux new-session -d -s "$NAME_SESSION"

tmux set-option -t "$NAME_SESSION" base-index 1
tmux set-option -t "$NAME_SESSION" pane-base-index 1

tmux set-hook -t "$NAME_SESSION" after-new-window[0] "send-keys 'source ${PROJECT_DIR}/.venv/bin/activate' Enter"
tmux set-hook -t "$NAME_SESSION" after-new-window[1] "send-keys 'clear' Enter"
tmux set-hook -t "$NAME_SESSION" after-split-window[0] "send-keys 'source ${PROJECT_DIR}/.venv/bin/activate' Enter"
tmux set-hook -t "$NAME_SESSION" after-split-window[1] "send-keys 'clear' Enter"

tmux send-keys -t "$NAME_SESSION:1.1" "source ${PROJECT_DIR}/.venv/bin/activate" Enter
if [ -f pyproject.toml ]; then
    tmux send-keys -t "$NAME_SESSION:1.1" "pip install --no-cache-dir -e '.[dev]'" Enter
fi
if [ -f requirements.txt ]; then
    tmux send-keys -t "$NAME_SESSION:1.1" "pip install --no-cache-dir -r requirements.txt" Enter
fi
tmux send-keys -t "$NAME_SESSION:1.1" "clear" Enter

tmux attach -t "$NAME_SESSION:1.1"
