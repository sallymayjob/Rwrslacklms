# Rwrslacklms

This repository contains an n8n workflow definition for Slack supervisor routing.

## Workflow behavior

- `url_verification` requests are routed through a challenge-only path.
- Challenge payloads are normalized to:
  - `type: "challenge"`
  - `challenge: <incoming challenge value>`
- Challenge responses return the dynamic challenge value with HTTP `200` and `application/json`.
- Non-challenge slash/event requests use a separate ACK response path (`{"status":"ok"}`).

See `supervisor_workflow.json`.
## Backup Apps Script example

Canonical lesson IDs use this format:

- `M##-W##-L##`

DEEP lessons remain parser-compatible by keeping the same canonical pattern and storing
`lesson_type: DEEP` in lesson metadata. For DEEP lessons, the canonical lesson number is `00`
(e.g. `M01-W00-L00`).

Legacy IDs such as `M01-W00-DEEP` are accepted by parsing and submit validation, then normalized
to canonical IDs for routing/reporting.
Command routing and agent workflow mapping for 12 supported slash commands.

## Validate command map

```bash
node tests/commandMap.test.js
```
