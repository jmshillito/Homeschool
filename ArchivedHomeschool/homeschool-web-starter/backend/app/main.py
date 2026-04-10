from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import BaselineResult, Goal, LearnerProfile, ProgressEntry
from .store import add_row, list_rows

app = FastAPI(title="Homeschool Web Starter")

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/learners")
def get_learners():
    return list_rows("learners")


@app.post("/api/learners")
def create_learner(payload: LearnerProfile):
    return add_row("learners", payload.model_dump(exclude_none=True))


@app.get("/api/baselines")
def get_baselines():
    return list_rows("baselines")


@app.post("/api/baselines")
def create_baseline(payload: BaselineResult):
    return add_row("baselines", payload.model_dump())


@app.get("/api/goals")
def get_goals():
    return list_rows("goals")


@app.post("/api/goals")
def create_goal(payload: Goal):
    return add_row("goals", payload.model_dump())


@app.get("/api/progress")
def get_progress():
    return list_rows("progress")


@app.post("/api/progress")
def create_progress(payload: ProgressEntry):
    return add_row("progress", payload.model_dump())
