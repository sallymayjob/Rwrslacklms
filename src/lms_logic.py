"""Submit validation and progress calculations built on canonical lesson IDs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .lesson_ids import parse_lesson_id, normalize_submit_token


@dataclass(frozen=True)
class SubmitPayload:
    user_id: str
    lesson_token: str


def validate_submit(payload: SubmitPayload) -> str:
    """Validate submit payload and return canonical lesson_id."""

    if not payload.user_id:
        raise ValueError("user_id is required")

    canonical_id = normalize_submit_token(payload.lesson_token)
    # parse to ensure routing/reporting can safely extract indexes
    parse_lesson_id(canonical_id)
    return canonical_id


def completion_percentage(completed_lesson_tokens: Iterable[str], total_lessons: int) -> float:
    """Compute progress using canonical IDs and legacy-compatible normalization."""

    if total_lessons <= 0:
        return 0.0

    unique_completed = {normalize_submit_token(token) for token in completed_lesson_tokens}
    return min(100.0, (len(unique_completed) / total_lessons) * 100.0)
