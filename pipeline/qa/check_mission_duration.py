#!/usr/bin/env python3
"""Validate lesson mission durations against tier limits and write verdict metadata."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "policy" / "mission_duration_policy.json"
LESSONS_DIR = ROOT / "lessons"
VERDICTS_PATH = ROOT / "data" / "qa" / "mission_duration_verdicts.json"


@dataclass
class Verdict:
    lesson_id: str
    tier: str
    duration_minutes: int
    limit_minutes: int
    policy_version: str
    status: str
    rule_id: str
    evaluated_at: str
    details: str


def load_policy() -> Dict[str, object]:
    return json.loads(POLICY_PATH.read_text())


def load_lessons() -> List[Dict[str, object]]:
    lessons: List[Dict[str, object]] = []
    for path in sorted(LESSONS_DIR.glob("**/*.json")):
        lessons.append(json.loads(path.read_text()))
    return lessons


def evaluate(policy: Dict[str, object], lessons: List[Dict[str, object]]) -> Dict[str, object]:
    limits: Dict[str, int] = policy["tier_limits_minutes"]
    compare = policy["comparison"]
    evaluated_at = datetime.now(timezone.utc).isoformat()

    verdicts: List[Dict[str, object]] = []
    failures = 0

    for lesson in lessons:
        tier = lesson["tier"]
        lesson_id = lesson["lesson_id"]
        duration = lesson["mission"]["duration_minutes"]
        limit = limits[tier]

        if compare == "strictly_less_than":
            passed = duration < limit
            requirement = f"duration < {limit}"
        else:
            passed = duration <= limit
            requirement = f"duration <= {limit}"

        status = "pass" if passed else "fail"
        if not passed:
            failures += 1

        verdict = Verdict(
            lesson_id=lesson_id,
            tier=tier,
            duration_minutes=duration,
            limit_minutes=limit,
            policy_version=policy["policy_version"],
            status=status,
            rule_id="mission-duration-by-tier",
            evaluated_at=evaluated_at,
            details=requirement,
        )
        verdicts.append(verdict.__dict__)

    return {
        "policy_version": policy["policy_version"],
        "rule": {
            "id": "mission-duration-by-tier",
            "description": "Fail lessons when mission duration exceeds the configured tier threshold.",
            "comparison": compare,
        },
        "generated_at": evaluated_at,
        "summary": {
            "total_lessons": len(verdicts),
            "pass": len(verdicts) - failures,
            "fail": failures,
        },
        "verdicts": verdicts,
    }


def main() -> int:
    policy = load_policy()
    lessons = load_lessons()
    result = evaluate(policy, lessons)

    VERDICTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    VERDICTS_PATH.write_text(json.dumps(result, indent=2) + "\n")

    print(f"Wrote {VERDICTS_PATH.relative_to(ROOT)}")
    if result["summary"]["fail"] > 0:
        print("Mission duration QA failed.")
        return 1

    print("Mission duration QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
