#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, List
from urllib import error, request


def http_json(method: str, url: str, payload: Dict[str, Any] | None = None) -> tuple[int, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            try:
                parsed = json.loads(body) if body else None
            except json.JSONDecodeError:
                parsed = body
            return resp.status, parsed
    except error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            parsed = json.loads(body) if body else None
        except json.JSONDecodeError:
            parsed = body
        return e.code, parsed
    except Exception as e:
        return 0, {"error": str(e)}


def print_result(label: str, status: int, data: Any) -> None:
    ok = 200 <= status < 300
    marker = "OK" if ok else "FAIL"
    print(f"\n[{marker}] {label} -> HTTP {status}")
    if data is not None:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def find_learner(learners: List[Dict[str, Any]], learner_id: str) -> Dict[str, Any] | None:
    for learner in learners:
        if str(learner.get("id")) == learner_id:
            return learner
    return None


def filter_records(records: List[Dict[str, Any]], learner_id: str) -> List[Dict[str, Any]]:
    matches = []
    for item in records:
        if str(item.get("learner_id")) == learner_id:
            matches.append(item)
    return matches


def sample_baselines(learner_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "learner_id": learner_id,
            "subject": "language",
            "band": "Developing",
            "notes": "Reads with reasonable fluency; inference and written summarising need support.",
        },
        {
            "learner_id": learner_id,
            "subject": "maths",
            "band": "Emerging",
            "notes": "Can complete number facts, but struggles to decode word-problem language and multi-step tasks.",
        },
        {
            "learner_id": learner_id,
            "subject": "science",
            "band": "Secure",
            "notes": "Explains observations well verbally and enjoys hands-on investigation.",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check homeschool API endpoints for a specific learner ID and optionally post sample baseline records.")
    parser.add_argument("learner_id", help="Learner ID to test")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL for the running API")
    parser.add_argument("--post-samples", action="store_true", help="POST three sample baseline records for the learner")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    print(f"Testing API at: {base}")
    print(f"Learner ID: {args.learner_id}")

    status, learners = http_json("GET", f"{base}/api/learners")
    print_result("GET /api/learners", status, learners)
    if not (200 <= status < 300) or not isinstance(learners, list):
        print("\nCannot continue until /api/learners returns a JSON list.")
        return 1

    learner = find_learner(learners, args.learner_id)
    if learner:
        print(f"\nMatched learner: {learner.get('display_name', '(no name)')}")
    else:
        print("\nWARNING: learner ID not found in /api/learners. Continuing anyway so you can test endpoint behavior.")

    for path in ["/api/baselines", "/api/goals", "/api/progress"]:
        status, records = http_json("GET", f"{base}{path}")
        label = f"GET {path}"
        if isinstance(records, list):
            filtered = filter_records(records, args.learner_id)
            print_result(label, status, {"matching_records": filtered, "count": len(filtered)})
        else:
            print_result(label, status, records)

    if args.post_samples:
        print("\nPosting sample baseline records...")
        for payload in sample_baselines(args.learner_id):
            status, data = http_json("POST", f"{base}/api/baselines", payload)
            print_result(f"POST /api/baselines [{payload['subject']} ]", status, data)

        status, records = http_json("GET", f"{base}/api/baselines")
        if isinstance(records, list):
            filtered = filter_records(records, args.learner_id)
            print_result("GET /api/baselines after sample POSTs", status, {"matching_records": filtered, "count": len(filtered)})
        else:
            print_result("GET /api/baselines after sample POSTs", status, records)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
