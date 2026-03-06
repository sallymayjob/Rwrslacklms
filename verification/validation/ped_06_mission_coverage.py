"""PED-06 validation: mission requirement vs verification coverage gap detector."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ValidationResult:
    check_id: str
    passed: bool
    missing_requirements: List[str]
    message: str


PED_06_REQUIRED_FIELDS = {
    "doc_link": "Document link",
    "goals_day_30": "Day 30 goal summary",
    "goals_day_60": "Day 60 goal summary",
    "goals_day_90": "Day 90 goal summary",
    "relationship_goal_month_1": "Month 1 relationship goal",
    "relationship_goal_month_2": "Month 2 relationship goal",
    "relationship_goal_month_3": "Month 3 relationship goal",
}

PED_06_MANAGER_SHARE_PATHS = {
    "manager_share_evidence": "Manager share evidence",
    "manager_share_structured_confirmation": "Manager structured confirmation",
}


def _is_present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, set, tuple)):
        return bool(value)
    return True


def run_ped_06_mission_coverage_check(verification_payload: Dict[str, object]) -> ValidationResult:
    """Validate that verification covers all mission requirements.

    The check fails when one or more mandatory mission fields are absent.
    Manager-share requirement passes when either direct evidence is present,
    or structured confirmation is present (privacy-compatible path).
    """

    missing: List[str] = []

    for field_name, field_label in PED_06_REQUIRED_FIELDS.items():
        if not _is_present(verification_payload.get(field_name)):
            missing.append(field_label)

    has_evidence = _is_present(verification_payload.get("manager_share_evidence"))
    has_structured_confirmation = _is_present(
        verification_payload.get("manager_share_structured_confirmation")
    )
    if not (has_evidence or has_structured_confirmation):
        missing.append(
            "Manager share confirmation (direct evidence or privacy-safe structured confirmation)"
        )

    passed = not missing
    message = (
        "PED-06 passed: verification covers all required mission elements."
        if passed
        else "PED-06 failed: verification is missing required mission elements."
    )

    return ValidationResult(
        check_id="PED-06",
        passed=passed,
        missing_requirements=missing,
        message=message,
    )
