from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "learners": DATA_DIR / "learners.json",
    "baselines": DATA_DIR / "baselines.json",
    "goals": DATA_DIR / "goals.json",
    "progress": DATA_DIR / "progress.json",
}


def _read(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _write(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2))


def list_rows(kind: str) -> List[Dict[str, Any]]:
    return _read(FILES[kind])


def add_row(kind: str, row: Dict[str, Any]) -> Dict[str, Any]:
    rows = _read(FILES[kind])
    row = {"id": str(uuid4()), **row}
    rows.append(row)
    _write(FILES[kind], rows)
    return row
