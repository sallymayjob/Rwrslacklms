#!/usr/bin/env python3
"""Validate workflow exports and fixtures for Slack secret leakage."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WORKFLOW_GLOBS = (
    "workflows/**/*.json",
    "fixtures/**/*.json",
    "**/*workflow*.json",
)

DISALLOWED_PATTERNS = {
    "Slack bot/user/app token": re.compile(r"xox[baprs]-[A-Za-z0-9-]+"),
    "Unredacted Slack webhook URL": re.compile(
        r"https://hooks\.slack\.com/(?!commands/\.\.\.REDACTED)[^\s\"']+"
    ),
    "Slack signing artifact": re.compile(
        r"(slack_signing_secret|x-slack-signature|v0=[a-f0-9]{16,})",
        re.IGNORECASE,
    ),
}

TRIGGER_TYPES = {
    "n8n-nodes-base.webhook",
    "n8n-nodes-base.manualTrigger",
}


def candidate_files() -> list[Path]:
    repo_root = Path.cwd()
    results: set[Path] = set()
    for pattern in WORKFLOW_GLOBS:
        results.update(repo_root.glob(pattern))
    return sorted(path for path in results if path.is_file())


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8")

    for label, regex in DISALLOWED_PATTERNS.items():
        if regex.search(raw):
            errors.append(f"{path}: detected {label}")

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
        return errors

    nodes = parsed.get("nodes", []) if isinstance(parsed, dict) else []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_type = node.get("type")
        node_name = node.get("name", "<unnamed>")
        if node_type in TRIGGER_TYPES and "pinData" in node:
            errors.append(
                f"{path}: trigger node '{node_name}' contains pinData; remove before sharing"
            )

    return errors


def main() -> int:
    paths = candidate_files()
    if not paths:
        print("No workflow JSON files found; nothing to validate.")
        return 0

    errors: list[str] = []
    for path in paths:
        errors.extend(check_file(path))

    if errors:
        print("Workflow validation failed:\n")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Validated {len(paths)} workflow JSON file(s); no Slack secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
