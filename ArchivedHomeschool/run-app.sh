#!/usr/bin/env bash
cd ~/projects/WebsiteMonitor/Homeschool/homeschool-web-starter || exit 1
source ../.venv/bin/activate
python -m uvicorn backend.app.main:app --reload