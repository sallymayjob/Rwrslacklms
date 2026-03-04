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
6. Deploy. Hostinger will build/run the stack and expose n8n on port `5678`.

You can start from the provided `.env.example` values and replace secrets before production use.

## What gets deployed

- `postgres` (PostgreSQL 16)
- `n8n` (latest)

The compose file already includes startup waiting logic so n8n only starts once Postgres is reachable.

## Verification updates

This repository now includes:

- Updated `property_verification` prompt requirements in [`verification/prompts/property_verification.md`](verification/prompts/property_verification.md).
- A PED-06 mission coverage validator in [`verification/validation/ped_06_mission_coverage.py`](verification/validation/ped_06_mission_coverage.py).
- Unit tests for PED-06 coverage logic in [`verification/validation/test_ped_06_mission_coverage.py`](verification/validation/test_ped_06_mission_coverage.py).
