#!/bin/bash
set -e

SESSION_NAME="mbird-console"

if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is not installed"
    exit 1
fi

echo "Starting mbird console..."

# Kill existing session if it exists
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true

# Create new session with backend
tmux new-session -d -s "$SESSION_NAME" -n backend -c "$(pwd)"
tmux send-keys -t "$SESSION_NAME:backend" "python -m mbird_console.main" C-m

# Create new window for frontend
tmux new-window -t "$SESSION_NAME" -n frontend -c "$(pwd)/frontend"
tmux send-keys -t "$SESSION_NAME:frontend" "npm run dev" C-m

echo ""
echo "✓ Backend and frontend started in tmux session '$SESSION_NAME'"
echo ""
echo "Open in browser: http://localhost:5173"
echo ""
echo "To attach to tmux session: tmux attach -t $SESSION_NAME"
echo "To switch windows in tmux: Ctrl-b then 0 (backend) or 1 (frontend)"
echo "To detach from tmux: Ctrl-b then d"
echo "To kill session: tmux kill-session -t $SESSION_NAME"
echo ""
