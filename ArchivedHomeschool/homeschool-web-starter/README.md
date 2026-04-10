# Homeschool Web Starter

A WSL-friendly starter project for turning the homeschool learning workflow into a website.

## Stack
- FastAPI backend
- Simple static frontend
- JSON file persistence for early prototyping

## Quick start in WSL

```bash
cd homeschool-web-starter
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Then open `http://127.0.0.1:8000` and `http://127.0.0.1:8000/docs`.

## What is included
- backend API skeleton
- simple frontend dashboard
- JSON schema examples
- project notes and roadmap

## Suggested next build order
1. lock the assessment schema
2. store baseline results
3. add goals and weekly targets
4. add progress charts
5. add exports and print views
