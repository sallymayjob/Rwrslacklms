from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


REQUIRED_METADATA_FIELDS = (
    "month_id",
    "audience",
    "lesson_created_at",
    "revision_count",
    "difficulty_tier",
)


class ValidationError(ValueError):
    """Raised when a record fails required-field validation."""


@dataclass
class ReadyRecord:
    lesson_id: str
    status: str
    month_id: str | None = None
    audience: str | None = None
    lesson_created_at: datetime | None = None
    revision_count: int | None = None
    difficulty_tier: str | None = None

    def required_field_errors(self) -> dict[str, str]:
        errors: dict[str, str] = {}

        if not self.month_id:
            errors["month_id"] = "month_id is required"
        if not self.audience:
            errors["audience"] = "audience is required"
        if not self.lesson_created_at:
            errors["lesson_created_at"] = "lesson_created_at is required"
        if self.revision_count is None:
            errors["revision_count"] = "revision_count is required"
        elif self.revision_count < 0:
            errors["revision_count"] = "revision_count must be >= 0"
        if not self.difficulty_tier:
            errors["difficulty_tier"] = "difficulty_tier is required"

        return errors

    def validate_required_metadata(self) -> None:
        errors = self.required_field_errors()
        if errors:
            pretty = ", ".join(f"{k}: {v}" for k, v in errors.items())
            raise ValidationError(
                f"Ready record {self.lesson_id} is missing required metadata: {pretty}"
            )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ReadyRecord":
        created_at = payload.get("lesson_created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return cls(
            lesson_id=payload["lesson_id"],
            status=payload.get("status", "Draft"),
            month_id=payload.get("month_id"),
            audience=payload.get("audience"),
            lesson_created_at=created_at,
            revision_count=payload.get("revision_count"),
            difficulty_tier=payload.get("difficulty_tier"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "lesson_id": self.lesson_id,
            "status": self.status,
            "month_id": self.month_id,
            "audience": self.audience,
            "lesson_created_at": self.lesson_created_at.isoformat()
            if self.lesson_created_at
            else None,
            "revision_count": self.revision_count,
            "difficulty_tier": self.difficulty_tier,
        }
