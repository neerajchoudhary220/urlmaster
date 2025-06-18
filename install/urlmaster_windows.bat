@echo off
cd /d %~dp0
call .venv\Scripts\activate.bat

start "" python main.py
cd public
start "" python -m http.server 8080
