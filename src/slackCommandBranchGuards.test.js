const assert = require('assert');
const {
  resolveRequesterTarget,
  buildImmediateAck,
  buildDeferredResponse,
  enforceAdminGuard,
} = require('./slackCommandBranchGuards');

const target = resolveRequesterTarget({ user_id: 'U123', channel_id: 'C1' });
assert.deepStrictEqual(target, { type: 'user', id: 'U123' });

const ack = buildImmediateAck('/report');
assert.strictEqual(ack.response_type, 'ephemeral');
assert.ok(ack.text.includes('/report'));

const deferred = buildDeferredResponse('/onboard', { childWorkflowName: 'child-onboard' });
assert.strictEqual(deferred.response_type, 'ephemeral');
assert.ok(deferred.text.includes('Delegating onboarding'));

const denied = enforceAdminGuard('/backup', { user_id: 'U2' }, ['U1']);
assert.strictEqual(denied.allowed, false);
assert.ok(denied.denial.text.includes('restricted to admins'));

const allowed = enforceAdminGuard('/backup', { user_id: 'U1' }, ['U1']);
assert.strictEqual(allowed.allowed, true);

console.log('All slack command guard tests passed.');
