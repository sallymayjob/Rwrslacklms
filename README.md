# Rwrslacklms

## Verification updates

This repository now includes:

- Updated `property_verification` prompt requirements in `verification/prompts/property_verification.md`.
- A PED-06 mission coverage validator in `verification/validation/ped_06_mission_coverage.py`.
- Unit tests for PED-06 coverage logic in `verification/validation/test_ped_06_mission_coverage.py`.


## Docker link deployment (Traefik + TLS)

This repo now includes `docker-compose.yml` for URL-based deployment.

### 1) Configure environment

```bash
cp .env.example .env
# edit .env with your real domain and secrets
```

Set DNS records before starting:
- `SUBDOMAIN.DOMAIN_NAME` -> server public IP (for n8n)
- `pgadmin.DOMAIN_NAME` -> server public IP (optional, for pgAdmin)

### 2) Start services

```bash
docker compose up -d
```

### 3) Access links

- n8n: `https://SUBDOMAIN.DOMAIN_NAME`
- pgAdmin: `https://pgadmin.DOMAIN_NAME`

Traefik automatically requests certificates using the TLS challenge.
