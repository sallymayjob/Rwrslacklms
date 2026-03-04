/**
 * Helpers for Slack command branch nodes.
 *
 * These helpers are intended for workflow engines (e.g. n8n code nodes) and
 * consolidate guardrails requested across command branches.
 */

const ADMIN_ONLY_COMMANDS = new Set(['/report', '/gaps', '/backup', '/onboard']);

/**
 * Resolve who should receive updates for a command execution.
 * Preference order:
 * 1) parsed payload user_id (requester identity)
 * 2) channel id fallback
 * 3) response_url fallback (for async response)
 */
function resolveRequesterTarget(payload = {}) {
  if (payload.user_id) {
    return { type: 'user', id: payload.user_id };
  }

  if (payload.channel_id) {
    return { type: 'channel', id: payload.channel_id };
  }

  if (payload.response_url) {
    return { type: 'response_url', id: payload.response_url };
  }

  return { type: 'unknown', id: null };
}

/**
 * Dynamic content factory per command.
 * If a command depends on child workflows, this function can return a
 * delegation marker instead of placeholder text.
 */
function buildCommandMessage(command, context = {}) {
  const user = context.userDisplay || context.user_id || 'there';

  switch (command) {
    case '/report':
      return `Generating your report now, <@${user}>. I'll share results shortly.`;
    case '/gaps':
      return `Checking coverage gaps for you, <@${user}>.`;
    case '/backup':
      return `Starting backup sequence requested by <@${user}>.`;
    case '/onboard':
      return context.childWorkflowName
        ? `Delegating onboarding to workflow \"${context.childWorkflowName}\".`
        : `Preparing onboarding steps for <@${user}>.`;
    default:
      return context.dynamicText || `Processing ${command} for <@${user}>.`;
  }
}

/**
 * Immediate ephemeral ack payload for slash commands.
 */
function buildImmediateAck(command, context = {}) {
  return {
    response_type: 'ephemeral',
    text:
      context.ackText ||
      `Received ${command}. Working on it now — I'll post an update when complete.`,
  };
}

/**
 * Deferred response payload for response_url callback.
 */
function buildDeferredResponse(command, context = {}) {
  return {
    response_type: context.responseType || 'ephemeral',
    replace_original: false,
    text: buildCommandMessage(command, context),
  };
}

/**
 * Admin-only guardrail check.
 */
function enforceAdminGuard(command, payload = {}, adminUserIds = []) {
  if (!ADMIN_ONLY_COMMANDS.has(command)) {
    return { allowed: true };
  }

  const isAdmin = adminUserIds.includes(payload.user_id);
  if (isAdmin) {
    return { allowed: true };
  }

  return {
    allowed: false,
    denial: {
      response_type: 'ephemeral',
      text: `Sorry <@${payload.user_id || 'unknown'}>, ${command} is restricted to admins.`,
    },
  };
}

module.exports = {
  ADMIN_ONLY_COMMANDS,
  resolveRequesterTarget,
  buildCommandMessage,
  buildImmediateAck,
  buildDeferredResponse,
  enforceAdminGuard,
};
