# Rwrslacklms

Utilities for Slack slash-command branch handling.

## Included guardrails

- Dynamic requester targeting using `user_id` (fallback: `channel_id`, then `response_url`).
- Dynamic command messages per command (or workflow delegation message).
- Immediate ephemeral acknowledgement payloads for slash commands.
- Deferred response payload builder for `response_url` callbacks.
- Admin-only protection for `/report`, `/gaps`, `/backup`, `/onboard`.

## Quick check

```bash
node src/slackCommandBranchGuards.test.js
```
