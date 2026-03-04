# Rwrslacklms

This repository contains sanitized workflow export material for Slack automation.

## Sanitization rules enforced

- Webhook and Manual Trigger nodes must not include `pinData`.
- Sample values must be redacted placeholders only:
  - `TXXXX`
  - `UXXXX`
  - `https://hooks.slack.com/commands/...REDACTED`
- No Slack tokens, webhook URLs, or signing artifacts are allowed in workflow exports or fixtures.

## Pre-commit validation

A local pre-commit hook is provided in `.pre-commit-config.yaml` and runs:

```bash
python3 scripts/validate_workflow_exports.py
```

Set up with:

```bash
pip install pre-commit
pre-commit install
```
