#!/usr/bin/env python3
"""Migrate lesson records and Slack submit command templates to canonical DEEP IDs.

Usage:
  python scripts/migrate_deep_ids.py input.json output.json

Input format:
  {
    "lessons": [{"lesson_id": "M01-W00-DEEP", ...}],
    "slack_submit_commands": ["/submit M01-W00-DEEP", ...]
  }
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from src.lesson_ids import parse_lesson_id


def migrate_payload(payload: dict) -> dict:
    migrated = dict(payload)

    lessons = []
    for lesson in payload.get("lessons", []):
        lesson = dict(lesson)
        parsed = parse_lesson_id(lesson["lesson_id"])
        lesson["lesson_id"] = parsed.lesson_id
        lesson.setdefault("lesson_type", parsed.lesson_type)
        lessons.append(lesson)
    migrated["lessons"] = lessons

    commands = []
    for command in payload.get("slack_submit_commands", []):
        parts = command.strip().split()
        if len(parts) >= 2 and parts[0] == "/submit":
            parsed = parse_lesson_id(parts[1])
            parts[1] = parsed.lesson_id
            commands.append(" ".join(parts))
        else:
            commands.append(command)
    migrated["slack_submit_commands"] = commands

    return migrated


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/migrate_deep_ids.py input.json output.json")
        return 1

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    payload = json.loads(in_path.read_text())
    migrated = migrate_payload(payload)
    out_path.write_text(json.dumps(migrated, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
