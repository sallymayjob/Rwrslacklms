# Rwrslacklms

## n8n Supervisor Webhook — How It Works

When Slack calls your n8n supervisor webhook, treat **authentication and freshness** as mandatory checks before any business logic executes.

### Required request validation (in order)

1. **Timestamp freshness check** using `X-Slack-Request-Timestamp`.
   - Parse the header as a Unix epoch (seconds).
   - Compare to current server time.
   - Enforce a strict tolerance window (commonly **±5 minutes / 300 seconds**).
   - Reject stale or far-future timestamps to prevent replay attacks.
2. **Signature validation** using `X-Slack-Signature` and your Slack signing secret.
   - Build the base string: `v0:{timestamp}:{raw_request_body}`.
   - Compute `HMAC-SHA256(signing_secret, base_string)` and prefix with `v0=`.
   - Compare using constant-time equality.

> Do not skip timestamp checking. A valid signature on an old payload is still unsafe.

### Explicit reject behavior

If validation fails, stop processing immediately and return an error response.

- **HTTP status**: `401 Unauthorized`
- **Response body** (example):
  ```json
  {
    "ok": false,
    "error": "invalid_request"
  }
  ```
- **Log fields required**:
  - `request_id`
  - `event_type` (if present; otherwise `unknown`)
  - `reason_rejected` (`timestamp_stale`, `timestamp_invalid`, `signature_mismatch`, etc.)

### Validation pseudo-code (timestamp + signature)

```pseudo
function handleSlackWebhook(request):
    request_id = request.header("X-Request-Id") or generateRequestId()
    event_type = parseEventType(request.rawBody) or "unknown"

    ts_raw = request.header("X-Slack-Request-Timestamp")
    sig = request.header("X-Slack-Signature")

    if ts_raw is missing or not integer:
        log.warn({request_id, event_type, reason_rejected: "timestamp_invalid"})
        return 401, {ok: false, error: "invalid_request"}

    ts = int(ts_raw)
    now = unixTimeSeconds()
    tolerance = 300  // 5 minutes

    if abs(now - ts) > tolerance:
        log.warn({request_id, event_type, reason_rejected: "timestamp_stale"})
        return 401, {ok: false, error: "invalid_request"}

    base = "v0:" + ts_raw + ":" + request.rawBody
    expected = "v0=" + hex(hmac_sha256(SLACK_SIGNING_SECRET, base))

    if not constantTimeEquals(expected, sig):
        log.warn({request_id, event_type, reason_rejected: "signature_mismatch"})
        return 401, {ok: false, error: "invalid_request"}

    // Request is authentic and fresh; continue normal webhook handling.
    return processEvent(request)
```
