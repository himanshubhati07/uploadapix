#!/usr/bin/env bash
set -e
export PORT=${PORT:-50619}
export PYTHONUNBUFFERED=1

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt -q

exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
