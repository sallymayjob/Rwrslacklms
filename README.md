# Rwrslacklms

## Lesson ID convention

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
