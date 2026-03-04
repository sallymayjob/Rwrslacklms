from __future__ import annotations

from .models import ReadyRecord


def mark_publish_ready(record: ReadyRecord) -> ReadyRecord:
    """Export/router layer gate to prevent incomplete Ready records."""
    record.validate_required_metadata()
    record.status = "Ready"
    return record
