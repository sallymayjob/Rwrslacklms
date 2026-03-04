const commandRoutes = {
  '/help': 'help_agent_workflow',
  '/status': 'status_agent_workflow',
  '/deploy': 'deploy_agent_workflow',
  '/rollback': 'rollback_agent_workflow',
  '/logs': 'logs_agent_workflow',
  '/metrics': 'metrics_agent_workflow',
  '/alerts': 'alerts_agent_workflow',
  '/incident': 'incident_agent_workflow',
  '/kb': 'kb_agent_workflow',
  '/runbook': 'runbook_agent_workflow',
  '/oncall': 'oncall_agent_workflow',
  '/handoff': 'handoff_agent_workflow',
};

module.exports = {
  commandRoutes,
};
