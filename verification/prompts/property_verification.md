# property_verification

Use this prompt when validating that a learner completed the mission plan deliverable.

## Required evidence (all elements required)

A verification response is only complete when it includes **all** of the following:

1. **Document link**
   - A working URL or file location to the learner's mission document.

2. **Day 30 / 60 / 90 goal summary**
   - Concise summary of goals for each milestone period:
     - Day 30
     - Day 60
     - Day 90

3. **Relationship goals by month**
   - Exactly one relationship goal for each month in scope:
     - Month 1 relationship goal
     - Month 2 relationship goal
     - Month 3 relationship goal

4. **Manager share confirmation / evidence**
   - Preferred: direct evidence that the document was shared with the manager (for example, screenshot, message permalink, email thread, signed confirmation, or LMS artifact).
   - Privacy-safe alternative: if direct evidence is restricted, accept a structured text confirmation with all required fields:
     - `manager_share_confirmed`: `true`
     - `privacy_constraint_reason`: short explanation of why direct evidence cannot be submitted
     - `share_channel`: where the share occurred (email/chat/meeting/LMS)
     - `share_date`: ISO date (`YYYY-MM-DD`)
     - `manager_identifier`: manager name or role identifier

## Verifier decision rule

- Mark as **pass** only if every required element above is present.
- If any required element is missing, mark as **needs_revision** and list each missing field explicitly.

## Output format

Return structured JSON:

```json
{
  "status": "pass | needs_revision",
  "missing_requirements": ["..."],
  "notes": "..."
}
```
