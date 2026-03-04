# Rwrslacklms

## Mission duration compliance

This repository enforces mission duration policy by tier via:

- Source of truth policy: `policy/mission_duration_policy.json`
- QA rule: `pipeline/qa/check_mission_duration.py`
- Verdict metadata output: `data/qa/mission_duration_verdicts.json`

Run:

```bash
python3 pipeline/qa/check_mission_duration.py
```

The command exits non-zero when any lesson mission exceeds its tier limit.
