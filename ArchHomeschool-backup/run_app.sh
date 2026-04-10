#!/usr/bin/env bash
cd "$(dirname "$0")/homeschool-web-starter" || exit 1
if [ -f ../.venv/bin/activate ]; then
  source ../.venv/bin/activate
elif [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f "$HOME/projects/WebsiteMonitor/Homeschool/.venv/bin/activate" ]; then
  source "$HOME/projects/WebsiteMonitor/Homeschool/.venv/bin/activate"
fi
python -m uvicorn backend.app.main:app --reload
