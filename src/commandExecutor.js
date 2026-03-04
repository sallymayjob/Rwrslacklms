const { commandRoutes } = require('./commandRoutes');
const { agentWorkflows } = require('./agentWorkflows');

function getExecutionPathForCommand(command) {
  const workflowId = commandRoutes[command];

  if (!workflowId) {
    return {
      ok: false,
      message: `No route is configured for command: ${command}`,
      executionPath: [],
    };
  }

  const workflow = agentWorkflows[workflowId];

  if (!workflow || !workflow.enabled || !Array.isArray(workflow.executeWorkflow) || workflow.executeWorkflow.length === 0) {
    return {
      ok: false,
      message: `Workflow '${workflowId}' is currently unavailable. Please try again later or contact support.`,
      executionPath: [],
    };
  }

  return {
    ok: true,
    message: `Workflow '${workflowId}' is ready.`,
    executionPath: workflow.executeWorkflow,
  };
}

module.exports = {
  getExecutionPathForCommand,
};
