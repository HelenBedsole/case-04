import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Mapping, Any

RESULTS_PATH = Path("data/survey.ndjson")

def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def append_json_line(record: Mapping[str, Any]) -> None:
    record = dict(record)
    if "email" in record and record["email"] is not None:
        record["email"] = _sha256(record["email"])
    if "age" in record and record["age"] is not None:
        record["age"] = _sha256(str(record["age"]))



    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
                default=lambda o: o.isoformat() if isinstance(o, datetime) else o
            ) + "\n"
        )
