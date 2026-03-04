const crypto = require('crypto');

const ALLOWED_TIMESTAMP_SKEW_SECONDS = 60 * 5;

function getHeader(headers, name) {
  if (!headers || typeof headers !== 'object') return undefined;
  const lower = name.toLowerCase();
  for (const [key, value] of Object.entries(headers)) {
    if (key.toLowerCase() === lower) return Array.isArray(value) ? value[0] : value;
  }
  return undefined;
}

function getRawBody(item) {
  if (Buffer.isBuffer(item?.rawBody)) return item.rawBody;
  if (typeof item?.rawBody === 'string') return Buffer.from(item.rawBody, 'utf8');

  if (Buffer.isBuffer(item?.body)) return item.body;
  if (typeof item?.body === 'string') return Buffer.from(item.body, 'utf8');
  if (item?.body && typeof item.body === 'object') {
    return Buffer.from(JSON.stringify(item.body));
  }

  if (Buffer.isBuffer(item?.request?.rawBody)) return item.request.rawBody;
  if (typeof item?.request?.rawBody === 'string') return Buffer.from(item.request.rawBody, 'utf8');

  return Buffer.from('');
}

function safeCompare(a, b) {
  const aBuffer = Buffer.from(String(a), 'utf8');
  const bBuffer = Buffer.from(String(b), 'utf8');

  if (aBuffer.length !== bBuffer.length) {
    return false;
  }

  return crypto.timingSafeEqual(aBuffer, bBuffer);
}

function verifySlackRequest({ headers, rawBody, signingSecret, now = Date.now() }) {
  if (!signingSecret) {
    return {
      valid: false,
      statusCode: 401,
      reason: 'Missing Slack signing secret',
      response: { ok: false, error: 'unauthorized' },
    };
  }

  const signature = getHeader(headers, 'X-Slack-Signature');
  const timestamp = getHeader(headers, 'X-Slack-Request-Timestamp');

  if (!signature || !timestamp) {
    return {
      valid: false,
      statusCode: 401,
      reason: 'Missing Slack signature headers',
      response: { ok: false, error: 'unauthorized' },
    };
  }

  const timestampSeconds = Number.parseInt(timestamp, 10);
  if (!Number.isFinite(timestampSeconds)) {
    return {
      valid: false,
      statusCode: 401,
      reason: 'Invalid Slack request timestamp',
      response: { ok: false, error: 'unauthorized' },
    };
  }

  const skewSeconds = Math.abs(Math.floor(now / 1000) - timestampSeconds);
  if (skewSeconds > ALLOWED_TIMESTAMP_SKEW_SECONDS) {
    return {
      valid: false,
      statusCode: 401,
      reason: `Slack timestamp skew too large: ${skewSeconds}s`,
      response: { ok: false, error: 'unauthorized' },
    };
  }

  const baseString = `v0:${timestampSeconds}:${rawBody.toString('utf8')}`;
  const computed = `v0=${crypto.createHmac('sha256', signingSecret).update(baseString).digest('hex')}`;

  if (!safeCompare(computed, signature)) {
    return {
      valid: false,
      statusCode: 401,
      reason: 'Slack signature mismatch',
      response: { ok: false, error: 'unauthorized' },
    };
  }

  return {
    valid: true,
    statusCode: 200,
    reason: 'Slack request verified',
    response: { ok: true },
  };
}

/**
 * n8n Code node entrypoint for "Supervisor Router".
 *
 * Expected input: an item with request headers/body.
 * Signing secret is read from env/credentials (no hardcoded secret).
 */
function supervisorRouterCodeNode(items) {
  return items.map((item) => {
    const source = item.json ?? item;
    const headers = source.headers ?? source.request?.headers ?? {};
    const rawBody = getRawBody(source);
    const signingSecret =
      source.credentials?.slackSigningSecret ||
      source.env?.SLACK_SIGNING_SECRET ||
      process.env.SLACK_SIGNING_SECRET;

    const verification = verifySlackRequest({
      headers,
      rawBody,
      signingSecret,
    });

    if (!verification.valid) {
      console.warn(`[Supervisor Router] Unauthorized Slack request: ${verification.reason}`);
      return {
        json: {
          valid: false,
          statusCode: verification.statusCode,
          error: 'unauthorized',
          reason: verification.reason,
        },
      };
    }

    return {
      json: {
        ...source,
        valid: true,
      },
    };
  });
}

module.exports = {
  ALLOWED_TIMESTAMP_SKEW_SECONDS,
  getHeader,
  getRawBody,
  safeCompare,
  verifySlackRequest,
  supervisorRouterCodeNode,
};
