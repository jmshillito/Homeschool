from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import (
    BaselineResult,
    Goal,
    LearnerProfile,
    LearnerUpdate,
    ProgressEntry,
    ReadingBaselineAnalyzeRequest,
    ReadingBaselineGenerateRequest,
)
from .store import add_row, get_row, list_rows, update_row

app = FastAPI(title="Homeschool Web Starter")

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


PASSAGES: Dict[str, Dict[str, Any]] = {
    "age_10_12": {
        "passage_title": "The Lost Map",
        "developmental_band_target": "developing to secure",
        "passage_text": (
            "Noah was helping his grandfather clear out the attic when he found a small wooden box "
            "hidden behind a stack of books. Inside it was a folded piece of paper with faded lines "
            "and symbols. At first, it looked like a drawing, but when Noah opened it carefully, he "
            "realized it was a map. One corner had been torn away, and the writing was hard to read, "
            "but there was a mark near the river behind the old mill. Noah's grandfather smiled when "
            "he saw it and said he had not thought about that map in years. Noah wondered why his "
            "grandfather had kept it and what might be waiting at the place it showed."
        ),
        "administration_notes": [
            "Read the passage aloud to compare listening comprehension against reading performance.",
            "Then ask the learner to read the passage aloud and note hesitations, substitutions, skipped endings, and self-corrections.",
            "Ask one comprehension question at a time. Record the exact child response where possible.",
            "Treat this as a support-needs screen, not a diagnosis.",
        ],
        "questions": [
            {"question_type": "literal", "question": "What did Noah find in the attic?"},
            {"question_type": "literal", "question": "Why did Noah think the paper might be important?"},
            {"question_type": "vocabulary", "question": "What does the word 'faded' mean in this story?"},
            {"question_type": "inference", "question": "Why do you think Noah's grandfather smiled when he saw the map?"},
            {"question_type": "summary", "question": "Summarize the story in 2 or 3 sentences."},
        ],
    }
}


def _pick_passage(age: int) -> Dict[str, Any]:
    return PASSAGES["age_10_12"]


@app.get("/")
def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/learner.html")
def learner_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "learner.html")


@app.get("/language.html")
def language_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "language.html")


@app.get("/api/learners")
def get_learners():
    return list_rows("learners")


@app.get("/api/learners/{learner_id}")
def get_learner(learner_id: str):
    learner = get_row("learners", learner_id)
    if not learner:
        raise HTTPException(status_code=404, detail="Learner not found")
    return learner


@app.post("/api/learners")
def create_learner(payload: LearnerProfile):
    return add_row("learners", payload.model_dump(exclude_none=True))


@app.put("/api/learners/{learner_id}")
def update_learner(learner_id: str, payload: LearnerUpdate):
    learner = update_row("learners", learner_id, payload.model_dump(exclude_none=True))
    if not learner:
        raise HTTPException(status_code=404, detail="Learner not found")
    return learner


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


@app.post("/api/language/reading-baseline/generate")
def generate_reading_baseline(payload: ReadingBaselineGenerateRequest):
    pack = _pick_passage(payload.age)
    return {
        "learner_id": payload.learner_id,
        "age": payload.age,
        "country": payload.country,
        "domain": "language",
        "diagnostic": "reading_baseline_v1",
        "student_profile": {
            "developmental_band_target": pack["developmental_band_target"],
        },
        **pack,
        "scoring_guide": {
            "question_scores": {"2": "accurate and clear", "1": "partly correct or vague", "0": "incorrect or off-topic"},
            "bands": ["Emerging", "Developing", "Secure", "Advanced"],
        },
    }


def _classify_band(score: int, max_score: int) -> str:
    ratio = 0 if max_score == 0 else score / max_score
    if ratio < 0.35:
        return "Emerging"
    if ratio < 0.7:
        return "Developing"
    if ratio < 0.9:
        return "Secure"
    return "Advanced"


@app.post("/api/language/reading-baseline/analyze")
def analyze_reading_baseline(payload: ReadingBaselineAnalyzeRequest):
    observed_errors_text = " ".join(payload.observed_errors).lower()
    accuracy_text = payload.read_accuracy_notes.lower()
    fluency_text = payload.read_fluency_notes.lower()
    listening_text = f"{payload.listening_retell} {payload.listening_notes}".lower()
    parent_text = " ".join([
        payload.parent_attention_notes,
        payload.parent_frustration_notes,
        payload.parent_confidence_notes,
        payload.parent_extra_notes,
    ]).lower()

    question_score = 0
    literal_score = 0
    literal_max = 0
    infer_score = 0
    infer_max = 0
    vocab_score = 0
    vocab_max = 0
    summary_score = 0
    summary_max = 0

    for item in payload.question_responses:
        response = item.child_response.strip()
        qtype = item.question_type.lower()
        if qtype == "literal":
            literal_max += 2
            literal_score += 2 if len(response.split()) >= 4 else 1 if response else 0
        elif qtype == "vocabulary":
            vocab_max += 2
            vocab_score += 2 if len(response.split()) >= 3 else 1 if response else 0
        elif qtype == "inference":
            infer_max += 2
            infer_score += 2 if len(response.split()) >= 5 else 1 if response else 0
        elif qtype == "summary":
            summary_max += 2
            summary_score += 2 if len(response.split()) >= 10 else 1 if response else 0
        question_score += 2 if len(response.split()) >= 6 else 1 if response else 0

    decoding_band = "Secure"
    decoding_evidence = payload.read_accuracy_notes or "No read-aloud notes provided."
    if any(term in accuracy_text or term in observed_errors_text for term in ["guessed", "skip", "skipped", "struggle", "struggled", "error", "wrong", "hesitat"]):
        decoding_band = "Developing"
    if any(term in accuracy_text or term in observed_errors_text for term in ["many", "frequent", "unable", "very hard", "could not"]):
        decoding_band = "Emerging"

    fluency_band = "Secure"
    if any(term in fluency_text for term in ["slow", "word-by-word", "word by word", "little expression", "paused"]):
        fluency_band = "Developing"
    if any(term in fluency_text for term in ["very slow", "laboured", "laborious"]):
        fluency_band = "Emerging"

    oral_language_band = "Developing"
    if len(payload.listening_retell.split()) >= 12 or "understood" in listening_text or "clear" in listening_text:
        oral_language_band = "Secure"
    if len(payload.listening_retell.split()) >= 25:
        oral_language_band = "Advanced"

    literal_band = _classify_band(literal_score, max(literal_max, 1))
    vocab_band = _classify_band(vocab_score, max(vocab_max, 1))
    inference_band = _classify_band(infer_score, max(infer_max, 1))
    summary_band = _classify_band(summary_score, max(summary_max, 1))

    written_band = "Developing"
    if len(payload.written_response.split()) >= 18:
        written_band = "Secure"
    elif len(payload.written_response.split()) <= 3 and payload.written_response.strip():
        written_band = "Emerging"
    elif not payload.written_response.strip():
        written_band = "Emerging"

    likely_strengths: List[str] = []
    possible_barriers: List[str] = []
    supports: List[str] = []

    if oral_language_band in ["Secure", "Advanced"]:
        likely_strengths.append("Oral language appears stronger than print-based response.")
    if literal_band in ["Secure", "Advanced"]:
        likely_strengths.append("Literal recall is a relative strength.")
    if decoding_band in ["Developing", "Emerging"] and oral_language_band in ["Secure", "Advanced"]:
        possible_barriers.append("Signs may suggest decoding or reading fluency is limiting comprehension.")
        supports.extend([
            "Use short passages and repeated reading.",
            "Teach chunking of longer words and suffix endings explicitly.",
        ])
    if inference_band in ["Emerging", "Developing"]:
        possible_barriers.append("Inference language may be a current barrier.")
        supports.append("Use 'Why do you think...?' prompts with evidence sentence starters.")
    if any(term in parent_text for term in ["attention", "reminder", "distract", "skip line", "impulsive"]):
        possible_barriers.append("Attention or sequencing may be affecting performance and is worth monitoring.")
        supports.append("Present one question at a time and use finger tracking or a visual pointer.")
    if any(term in parent_text for term in ["frustrat", "avoid", "confidence"]):
        possible_barriers.append("Confidence and task persistence may be affecting performance.")
        supports.append("Keep tasks short and praise strategy use before accuracy.")
    if written_band in ["Emerging"] and oral_language_band in ["Secure", "Advanced"]:
        possible_barriers.append("Written expression may be masking what the learner understands orally.")
        supports.append("Allow oral rehearsal before writing and provide sentence starters.")

    if not supports:
        supports = [
            "Keep questions short and concrete.",
            "Model one worked example before independent responses.",
            "Use history, geography, or art topics as motivating reading vehicles.",
        ]

    subskills = {
        "oral_language": {
            "band": oral_language_band,
            "confidence": "Medium",
            "evidence": payload.listening_retell or payload.listening_notes or "Limited listening evidence provided.",
            "next_step": "Use oral retell before asking for written responses.",
        },
        "decoding": {
            "band": decoding_band,
            "confidence": "Medium",
            "evidence": decoding_evidence,
            "next_step": "Focus on longer words, endings, and decoding unfamiliar vocabulary.",
        },
        "fluency": {
            "band": fluency_band,
            "confidence": "Medium",
            "evidence": payload.read_fluency_notes or "Limited fluency evidence provided.",
            "next_step": "Practice repeated reading with short passages and phrasing.",
        },
        "vocabulary": {
            "band": vocab_band,
            "confidence": "Low" if vocab_max == 0 else "Medium",
            "evidence": f"Vocabulary responses score: {vocab_score}/{max(vocab_max, 1)}",
            "next_step": "Pre-teach key words before reading.",
        },
        "literal_comprehension": {
            "band": literal_band,
            "confidence": "Low" if literal_max == 0 else "High",
            "evidence": f"Literal response score: {literal_score}/{max(literal_max, 1)}",
            "next_step": "Ask who, what, where questions before moving to why questions.",
        },
        "inference": {
            "band": inference_band,
            "confidence": "Low" if infer_max == 0 else "Medium",
            "evidence": f"Inference response score: {infer_score}/{max(infer_max, 1)}",
            "next_step": "Use evidence-based sentence starters such as 'I think... because...'.",
        },
        "retell_summary": {
            "band": summary_band,
            "confidence": "Low" if summary_max == 0 else "Medium",
            "evidence": payload.written_response or payload.listening_retell or "Limited retell evidence provided.",
            "next_step": "Practice retelling with beginning-middle-end prompts.",
        },
        "written_response": {
            "band": written_band,
            "confidence": "Medium",
            "evidence": payload.written_response or "No written response provided.",
            "next_step": "Use oral rehearsal and sentence frames before independent writing.",
        },
    }

    overall = _classify_band(question_score, max(len(payload.question_responses) * 2, 1))
    if decoding_band == "Emerging" or fluency_band == "Emerging":
        overall = "Developing" if overall in ["Secure", "Advanced"] else overall

    return {
        "learner_id": payload.learner_id,
        "domain": "language",
        "diagnostic": "reading_baseline_v1",
        "overall_reading_band": overall,
        "subskills": subskills,
        "likely_strengths": likely_strengths,
        "possible_barriers": possible_barriers,
        "supports_to_trial": list(dict.fromkeys(supports)),
        "follow_up_flag": "Consider professional follow-up if concerns persist after 6 to 8 weeks of targeted support.",
        "caution": "This is a support-needs screen, not a diagnosis.",
    }
