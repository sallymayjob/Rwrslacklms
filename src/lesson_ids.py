"""Lesson ID parsing and validation helpers.

Canonical lesson IDs remain machine-parseable by the historic routing format:
    M##-W##-L##

DEEP lessons now use the same canonical ID pattern and are marked with
`lesson_type="DEEP"` in content metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, Any

CANONICAL_LESSON_ID_RE = re.compile(r"^M(?P<module>\d{2})-W(?P<week>\d{2})-L(?P<lesson>\d{2})$")
LEGACY_DEEP_ID_RE = re.compile(r"^M(?P<module>\d{2})-W(?P<week>\d{2})-DEEP$")
ALLOWED_LESSON_TYPES = {"STANDARD", "DEEP"}


@dataclass(frozen=True)
class LessonRef:
    module: int
    week: int
    lesson: int
    lesson_id: str
    lesson_type: str = "STANDARD"


def format_lesson_id(module: int, week: int, lesson: int) -> str:
    return f"M{module:02d}-W{week:02d}-L{lesson:02d}"


def parse_lesson_id(raw_id: str) -> LessonRef:
    """Parse canonical and legacy lesson IDs.

    Legacy DEEP IDs (M##-W##-DEEP) are normalized to M##-W##-L00.
    """

    canonical = CANONICAL_LESSON_ID_RE.match(raw_id)
    if canonical:
        module = int(canonical.group("module"))
        week = int(canonical.group("week"))
        lesson = int(canonical.group("lesson"))
        return LessonRef(module=module, week=week, lesson=lesson, lesson_id=raw_id)

    legacy_deep = LEGACY_DEEP_ID_RE.match(raw_id)
    if legacy_deep:
        module = int(legacy_deep.group("module"))
        week = int(legacy_deep.group("week"))
        normalized_id = format_lesson_id(module=module, week=week, lesson=0)
        return LessonRef(
            module=module,
            week=week,
            lesson=0,
            lesson_id=normalized_id,
            lesson_type="DEEP",
        )

    raise ValueError(f"Unsupported lesson id format: {raw_id}")


def validate_content_record(record: Dict[str, Any]) -> None:
    """Validate content schema before publish/export.

    Required keys:
      - lesson_id (must be canonical M##-W##-L##)
      - lesson_type (STANDARD|DEEP)
    """

    lesson_id = record.get("lesson_id")
    lesson_type = record.get("lesson_type", "STANDARD")

    if not isinstance(lesson_id, str) or not CANONICAL_LESSON_ID_RE.match(lesson_id):
        raise ValueError(
            f"Invalid lesson_id {lesson_id!r}. Required canonical format is M##-W##-L##"
        )

    if lesson_type not in ALLOWED_LESSON_TYPES:
        raise ValueError(
            f"Invalid lesson_type {lesson_type!r}. Allowed values: {sorted(ALLOWED_LESSON_TYPES)}"
        )

    parsed = parse_lesson_id(lesson_id)
    if lesson_type == "DEEP" and parsed.lesson != 0:
        raise ValueError("DEEP lessons must use lesson number 00 in canonical lesson_id")


def normalize_submit_token(raw_token: str) -> str:
    """Normalize submit command lesson token to canonical ID."""

    return parse_lesson_id(raw_token).lesson_id
