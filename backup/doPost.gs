/**
 * Receives backup payloads and writes RFC-4180-safe CSV snapshots to Drive.
 */
function doPost(e) {
  var payload = JSON.parse(e.postData.contents);
  var headers = payload.headers || [];
  var rows = payload.rows || [];

  var csvLines = [];
  csvLines.push(headers.map(toCsvCell).join(','));

  rows.forEach(function(row) {
    csvLines.push(row.map(toCsvCell).join(','));
  });

  var csv = csvLines.join('\r\n');
  var filename = 'backup-' + new Date().toISOString() + '.csv';

  // Export backups as UTF-8 so multilingual content round-trips correctly.
  var blob = Utilities.newBlob(csv, 'text/csv', filename).setDataFromString(csv, 'UTF-8');
  DriveApp.createFile(blob);

  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, file: filename }))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * RFC-4180-safe CSV cell serializer.
 * - Escapes embedded quotes by doubling them.
 * - Wraps fields containing commas/newlines/quotes in double quotes.
 */
function toCsvCell(value) {
  var cell = value == null ? '' : String(value);
  var escaped = cell.replace(/"/g, '""');

  if (/[",\r\n]/.test(cell)) {
    return '"' + escaped + '"';
  }

  return escaped;
}

/**
 * Restore verification tip:
 * After each backup export, run a sample import test (e.g., open the CSV in
 * your restore script and parse a row with commas/newlines/quotes) to confirm
 * the UTF-8 file parses correctly before relying on the backup.
 */
