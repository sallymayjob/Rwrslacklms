from __future__ import annotations

from datetime import date
from typing import Iterable

from .models import ReadyRecord


def generate_weekly_data_quality_report(
    records: Iterable[ReadyRecord], run_date: date | None = None
) -> dict:
    """Generate weekly report of lessons with missing required metadata."""
    run_date = run_date or date.today()
    incomplete = []

    for record in records:
        errors = record.required_field_errors()
        if errors:
            incomplete.append(
                {
                    "lesson_id": record.lesson_id,
                    "status": record.status,
                    "missing_fields": sorted(errors.keys()),
                }
            )

    return {
        "report_date": run_date.isoformat(),
        "incomplete_lessons": incomplete,
        "incomplete_count": len(incomplete),
    }
