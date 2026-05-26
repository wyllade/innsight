#!/bin/bash
# Start both backends in persistent tmux sessions
# Usage: bash start.sh

cd /home/emman/innsight

# Kill any existing sessions
tmux kill-session -t innsight-node 2>/dev/null
tmux kill-session -t innsight-py 2>/dev/null

# Node.js backend on port 3001
cd backend
tmux new-session -d -s innsight-node 'node server.js'
echo "Node.js backend starting on port 3001..."

cd ..

# Python backend on port 3002
cd python-backend
tmux new-session -d -s innsight-py 'python -m uvicorn app.main:app --port 3002'
echo "Python backend starting on port 3002..."

cd ..

# Wait and verify
sleep 2
echo ""
echo "=== Node.js ==="
curl -s http://localhost:3001/ | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','FAIL'))" 2>/dev/null || echo "FAILED"
echo "=== Python ==="
curl -s http://localhost:3002/ | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','FAIL'))" 2>/dev/null || echo "FAILED"
echo ""
echo "Attach: tmux attach -t innsight-node  (or innsight-py)"
