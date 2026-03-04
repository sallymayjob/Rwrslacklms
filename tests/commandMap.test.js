const assert = require('assert');
const { commandRoutes } = require('../src/commandRoutes');
const { agentWorkflows } = require('../src/agentWorkflows');
const { getExecutionPathForCommand } = require('../src/commandExecutor');

const commands = Object.keys(commandRoutes);

assert.strictEqual(commands.length, 12, `Expected 12 slash commands, found ${commands.length}`);

for (const command of commands) {
  const workflowId = commandRoutes[command];
  const workflow = agentWorkflows[workflowId];

  assert.ok(workflow, `${command} maps to missing workflow '${workflowId}'`);
  assert.strictEqual(workflow.enabled, true, `${command} maps to disabled workflow '${workflowId}'`);
  assert.ok(Array.isArray(workflow.executeWorkflow), `${workflowId} must provide executeWorkflow nodes`);
  assert.ok(workflow.executeWorkflow.length > 0, `${workflowId} executeWorkflow cannot be empty`);

  const result = getExecutionPathForCommand(command);
  assert.strictEqual(result.ok, true, `Execution path should be available for ${command}`);
  assert.ok(result.executionPath.length > 0, `${command} should return non-empty execution path`);
}

const unavailable = getExecutionPathForCommand('/unknown');
assert.strictEqual(unavailable.ok, false);
assert.ok(unavailable.message.includes('No route is configured'));

const original = agentWorkflows.help_agent_workflow;
agentWorkflows.help_agent_workflow = { enabled: false, executeWorkflow: [] };
const fallback = getExecutionPathForCommand('/help');
assert.strictEqual(fallback.ok, false);
assert.ok(fallback.message.includes('currently unavailable'));
agentWorkflows.help_agent_workflow = original;

console.log('All 12 command routes map to enabled workflows with non-empty executeWorkflow nodes.');
