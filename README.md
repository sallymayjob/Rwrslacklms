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
