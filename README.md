# Rwrslacklms

## Backup Apps Script example

See [`backup/doPost.gs`](backup/doPost.gs) for an updated `doPost` snippet that:

- uses RFC-4180-safe CSV escaping via `toCsvCell(value)`
- maps every header/data cell through `toCsvCell` before `join(',')`
- preserves line breaks safely with `\r\n` row delimiters
- writes backups as UTF-8 and includes a restore verification note (sample import test)
