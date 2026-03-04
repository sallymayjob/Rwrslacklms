# Environment Variables / Deployment Values (Internal Only)

> Restricted internal operator reference. Do not publish in broadly shared docs.

| Placeholder | Production value |
| --- | --- |
| `{{N8N_WEBHOOK_URL}}` | `https://n8n.srv1371300.hstgr.cloud/webhook/supervisor` |
| `{{LMS_ALERT_EMAIL}}` | `ld-lead@rwrgroup.com` |
| `{{BACKUP_FOLDER_ID}}` | `YOUR_BACKUP_FOLDER_ID` (replace with the real backup target ID used in production) |
| `{{SLACK_BOT_TOKEN}}` | `xoxb-your-bot-token` (replace with actual Slack bot token from secrets manager) |
| `{{PGADMIN_DEFAULT_EMAIL}}` | `admin+pgadmin-change-me@example.com` (set a unique operator-controlled mailbox in secrets manager) |
| `{{PGADMIN_DEFAULT_PASSWORD}}` | `CHANGEME_generate_32plus_char_unique_secret` (store only in secrets manager / `.env`, rotate regularly) |

## pgAdmin exposure hardening

- Avoid publishing pgAdmin directly with a raw host binding like `5050:80` when the stack is internet-exposed.
- Prefer routing pgAdmin through an authenticated reverse proxy rule-set (SSO/IP allow-list/MFA) and remove direct host port publication where possible.
