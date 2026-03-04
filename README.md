# Rwrslacklms

This repo is ready to deploy as a **single Git-link install** in Hostinger Docker Manager.

## One-link install on Hostinger Docker Manager

1. Push this repository to your Git provider (GitHub/GitLab/Bitbucket).
2. In **Hostinger → VPS → Docker Manager**, choose **Deploy from Git repository**.
3. Paste your repository URL.
4. Select `docker-compose.yml` as the deployment file.
5. Add environment variables in Hostinger (or from a `.env` file):
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`
   - `N8N_ENCRYPTION_KEY`
   - Optional but recommended: `N8N_HOST`, `N8N_PROTOCOL`, `N8N_EDITOR_BASE_URL`, `WEBHOOK_URL`, `GENERIC_TIMEZONE`
6. Deploy. Hostinger will run the stack and expose n8n on port `5678`.

### Fix for "This site can't be reached" (ERR_CONNECTION_TIMED_OUT)

If your browser times out when opening your server IP/domain, set these variables to match your public host:

- `N8N_HOST=0.0.0.0`
- `N8N_EDITOR_BASE_URL=http://<your-public-host-or-ip>:5678`
- `WEBHOOK_URL=http://<your-public-host-or-ip>:5678`

`N8N_HOST=0.0.0.0` ensures n8n listens on all interfaces in the container so Hostinger can publish port `5678` externally.

## Are all workflows imported automatically?

Yes. On first container start, n8n imports every `*.json` workflow from:

- `./workflows/`
- `./slack_post_ack_routing.workflow.json`

After a successful first import, a marker file (`/home/node/.n8n/.workflows_imported`) is written in the persistent `n8n_data` volume, so workflows are not imported again on every restart.

## What gets deployed

- `postgres` (PostgreSQL 16, persistent volume: `postgres_data`)
- `n8n` (latest, persistent volume: `n8n_data`)

The compose file includes startup waiting logic so n8n starts only after Postgres is reachable.

## Verification updates

This repository now includes:

- Updated `property_verification` prompt requirements in [`verification/prompts/property_verification.md`](verification/prompts/property_verification.md).
- A PED-06 mission coverage validator in [`verification/validation/ped_06_mission_coverage.py`](verification/validation/ped_06_mission_coverage.py).
- Unit tests for PED-06 coverage logic in [`verification/validation/test_ped_06_mission_coverage.py`](verification/validation/test_ped_06_mission_coverage.py).
