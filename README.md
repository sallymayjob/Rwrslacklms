# Rwrslacklms

Refactored n8n workflow for Slack LMS webhook routing is available in:

- `slack_post_ack_routing.workflow.json`

The workflow now:
- branches early by payload type (`challenge`, `command`, `interactive`, `event`),
- normalizes slash command fields in an enabled mapping node,
- routes commands through a dedicated switch map (`/learn`, `/submit`, `/status`), and
- sends webhook acknowledgment independently so asynchronous processing can continue.
