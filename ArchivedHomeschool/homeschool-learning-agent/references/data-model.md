# Web-ready data model

Use these entities for a homeschool website or app.

## Core entities

### learner_profile
- id
- display_name
- age
- country
- hours_per_week
- priorities
- observed_concerns
- strengths_interests
- preferred_vehicles
- created_at
- updated_at

### assessment_session
- id
- learner_id
- session_date
- assessor_name
- notes
- duration_minutes

### baseline_result
- id
- assessment_session_id
- domain
- subskill
- raw_evidence
- band
- confidence
- primary_barrier
- next_step
- vehicle_subject

### support_flag
- id
- learner_id
- area
- description
- severity_hint
- monitor_only

### goal
- id
- learner_id
- domain
- horizon_weeks
- goal_text
- baseline_band
- target_band
- support_strategy
- mastery_evidence
- status

### weekly_target
- id
- goal_id
- week_number
- target_text
- scaffold
- success_criteria
- vehicle_subject

### progress_entry
- id
- learner_id
- week_number
- domain
- minutes_spent
- engagement_score
- band
- success_notes
- barrier_notes
- parent_next_step
- recorded_at

## Minimal API suggestion
- GET /learners/:id
- POST /learners
- POST /assessment-sessions
- POST /baseline-results
- POST /goals
- POST /weekly-targets
- POST /progress-entries
- GET /reports/:learnerId/weekly-summary
- GET /reports/:learnerId/baseline-overview

## Example learner_profile JSON

```json
{
  "display_name": "Learner",
  "age": 10,
  "country": "Australia",
  "hours_per_week": 8,
  "priorities": ["reading confidence", "word problems"],
  "observed_concerns": ["forgets multistep instructions"],
  "strengths_interests": ["music", "drawing"],
  "preferred_vehicles": ["Art", "Music", "Geography"]
}
```

## Example baseline_result JSON

```json
{
  "domain": "Maths",
  "subskill": "Word problems",
  "raw_evidence": "Can calculate accurately but struggles to identify the operation.",
  "band": "Developing",
  "confidence": "Medium",
  "primary_barrier": "Language load",
  "next_step": "Restate the problem in own words before solving.",
  "vehicle_subject": "Geography"
}
```
