# Homeschool Web Starter

This starter now includes:
- learner home page with learner table and open-learner action
- learner hub page with subject tiles
- Language diagnostics page
- Reading baseline generation and analysis endpoints

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload
```

Open:
- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## New pages

- `/` home page
- `/learner.html?id=<learner-id>` learner hub with subject tiles
- `/language.html?id=<learner-id>` language diagnostics page

## New API endpoints

- `GET /api/learners/{learner_id}`
- `POST /api/language/reading-baseline/generate`
- `POST /api/language/reading-baseline/analyze`

## Suggested test flow

1. Create a learner on the home page.
2. Click **Open learner**.
3. Click the **Language** tile.
4. Click **Generate reading exercise**.
5. Enter read-aloud observations, child answers, and parent notes.
6. Click **Analyze reading baseline**.
7. Review the returned bands, strengths, barriers, and support ideas.

## Notes

The reading analysis uses a simple rule-based engine so the project has a stable internal structure before adding a live AI provider. Treat it as a support-needs screen, not a diagnosis.
