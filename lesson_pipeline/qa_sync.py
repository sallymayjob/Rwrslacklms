from __future__ import annotations

from typing import Iterable

from .models import ReadyRecord, ValidationError


def sync_ready_records(records: Iterable[ReadyRecord]) -> tuple[list[ReadyRecord], list[str]]:
    """QA sync stage gate: only fully populated Ready records can sync."""
    synced: list[ReadyRecord] = []
    blocked: list[str] = []

    for record in records:
        if record.status != "Ready":
            continue

        try:
            record.validate_required_metadata()
            synced.append(record)
        except ValidationError as exc:
            blocked.append(str(exc))

    return synced, blocked
