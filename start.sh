#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cleanup() {
  echo ""
  echo "Shutting down..."
  if [ -n "$BACKEND_PID" ]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
  exit 0
}
trap cleanup SIGINT SIGTERM

echo "=== Starting Innsight ==="

# Start backend
cd "$ROOT_DIR/backend"
rm -f instance/app.db
echo "[backend] Installing Python deps..."
pip install -q -r requirements.txt 2>/dev/null || true
echo "[backend] Starting Flask server on port 3001..."
python3 run.py &
BACKEND_PID=$!

# Wait for backend to be ready
for i in $(seq 1 15); do
  if curl -sL http://localhost:3001/api/hotels >/dev/null 2>&1; then
    echo "[backend] Ready"
    break
  fi
  sleep 1
done

# Start frontend
cd "$ROOT_DIR/frontend"
echo "[frontend] Installing npm deps..."
npm install --silent 2>/dev/null || true
echo "[frontend] Starting Vite dev server on port 3000..."
npx vite --host

cleanup
