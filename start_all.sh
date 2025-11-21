#!/usr/bin/env bash
set -euo pipefail

# Simple helper to build frontend and start backend (for local dev / simple deployment)
# Usage: ./start_all.sh

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Building frontend..."
cd "$ROOT_DIR/frontend"
npm install --no-audit --no-fund
npm run build

echo "Starting backend (uvicorn)..."
cd "$ROOT_DIR"
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
