from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .models import ReadyRecord

SAFE_DEFAULTS = {
    "revision_count": 0,
    "difficulty_tier": "unknown",
    "audience": "general",
}


def _recover_created_at(lesson_id: str, source_system: dict[str, dict]) -> datetime | None:
    source_lesson = source_system.get(lesson_id, {})
    created = source_lesson.get("lesson_created_at")
    if isinstance(created, datetime):
        return created
    if isinstance(created, str):
        return datetime.fromisoformat(created)
    return None


def backfill_ready_record(record: ReadyRecord, source_system: dict[str, dict]) -> ReadyRecord:
    """Backfill null metadata using source values first, then safe defaults."""
    source_lesson = source_system.get(record.lesson_id, {})

    if not record.month_id:
        record.month_id = source_lesson.get("month_id")
    if not record.audience:
        record.audience = source_lesson.get("audience", SAFE_DEFAULTS["audience"])
    if not record.lesson_created_at:
        record.lesson_created_at = _recover_created_at(record.lesson_id, source_system)
    if record.revision_count is None:
        record.revision_count = source_lesson.get(
            "revision_count", SAFE_DEFAULTS["revision_count"]
        )
    if not record.difficulty_tier:
        record.difficulty_tier = source_lesson.get(
            "difficulty_tier", SAFE_DEFAULTS["difficulty_tier"]
        )

    return record


def backfill_ready_records(
    records: Iterable[ReadyRecord], source_system: dict[str, dict]
) -> list[ReadyRecord]:
    return [backfill_ready_record(record, source_system) for record in records]
