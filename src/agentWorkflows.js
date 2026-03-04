const agentWorkflows = {
  help_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'resolveHelpTopic', 'renderHelpResponse'],
  },
  status_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadServiceStatus', 'renderStatusResponse'],
  },
  deploy_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadDeployTarget', 'runDeployment', 'renderDeploySummary'],
  },
  rollback_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadRollbackTarget', 'runRollback', 'renderRollbackSummary'],
  },
  logs_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadLogContext', 'fetchLogs', 'renderLogsSummary'],
  },
  metrics_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadMetricScope', 'fetchMetrics', 'renderMetricsSummary'],
  },
  alerts_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadAlertScope', 'fetchActiveAlerts', 'renderAlertsSummary'],
  },
  incident_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadIncidentContext', 'openIncidentTimeline', 'renderIncidentSummary'],
  },
  kb_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'resolveKnowledgeQuery', 'searchKnowledgeBase', 'renderKnowledgeResponse'],
  },
  runbook_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'resolveRunbook', 'renderRunbookSteps'],
  },
  oncall_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'resolveOncallSchedule', 'renderOncallResponse'],
  },
  handoff_agent_workflow: {
    enabled: true,
    executeWorkflow: ['parseCommand', 'loadShiftContext', 'renderHandoffSummary'],
  },

  // Obsolete chains removed from router coverage:
  // legacy_triage_workflow
  // legacy_lookup_workflow
};

module.exports = {
  agentWorkflows,
};
