@echo off
set PORT=48369
set PYTHONUNBUFFERED=1

if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt -q

uvicorn app.main:app --host 0.0.0.0 --port 48369
