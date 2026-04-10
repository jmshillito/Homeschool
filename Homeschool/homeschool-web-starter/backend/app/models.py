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
    preferred_vehicles: List[str] = Field(default_factory=list)


class LearnerUpdate(BaseModel):
    display_name: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None
    hours_per_week: Optional[int] = None
    priorities: Optional[List[str]] = None
    observed_concerns: Optional[List[str]] = None
    strengths_interests: Optional[List[str]] = None
    preferred_vehicles: Optional[List[str]] = None


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


class ReadingQuestionResponse(BaseModel):
    question_type: str
    question: str
    child_response: str


class ReadingBaselineGenerateRequest(BaseModel):
    learner_id: Optional[str] = None
    age: int
    country: str


class ReadingBaselineAnalyzeRequest(BaseModel):
    learner_id: Optional[str] = None
    age: int
    country: str
    passage_title: str
    listening_retell: str = ""
    listening_notes: str = ""
    read_accuracy_notes: str = ""
    read_fluency_notes: str = ""
    self_correction_notes: str = ""
    observed_errors: List[str] = Field(default_factory=list)
    question_responses: List[ReadingQuestionResponse] = Field(default_factory=list)
    written_response: str = ""
    parent_attention_notes: str = ""
    parent_frustration_notes: str = ""
    parent_confidence_notes: str = ""
    parent_extra_notes: str = ""
