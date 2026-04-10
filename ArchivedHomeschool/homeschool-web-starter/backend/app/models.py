from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class LearnerProfile(BaseModel):
    id: Optional[str] = None
    display_name: str = "Learner"
    age: int
    country: str
    hours_per_week: int = 8
    priorities: List[str] = Field(default_factory=list)
    observed_concerns: List[str] = Field(default_factory=list)
    strengths_interests: List[str] = Field(default_factory=list)
    preferred_vehicles: List[str] = Field(default_factory=lambda: ["Art", "IT", "Geography", "History", "Music"])


class BaselineResult(BaseModel):
    learner_id: str
    domain: str
    subskill: str
    raw_evidence: str
    band: str
    confidence: str
    primary_barrier: str = ""
    next_step: str = ""
    vehicle_subject: str = ""


class Goal(BaseModel):
    learner_id: str
    domain: str
    horizon_weeks: int = 12
    goal_text: str
    baseline_band: str
    target_band: str
    support_strategy: str = ""
    mastery_evidence: str = ""
    status: str = "active"


class ProgressEntry(BaseModel):
    learner_id: str
    week_number: int
    domain: str
    minutes_spent: int = 0
    engagement_score: int = 3
    band: str
    success_notes: str = ""
    barrier_notes: str = ""
    parent_next_step: str = ""
