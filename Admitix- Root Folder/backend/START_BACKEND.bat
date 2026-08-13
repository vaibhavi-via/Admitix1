@echo off
cd /d "%~dp0"
set "PYTHONPATH=.."
echo Starting Admitix backend on http://127.0.0.1:8000
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
