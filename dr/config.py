from __future__ import print_function
"""Runtime configuration for Security White-box Testing / Dependency Risk (SCA)."""
LANGUAGE = 'python'
RUNTIME_VERSION = '3.12'
PYTHON_VERSION = '3.12'
BRANCH_TYPE = 'Bug'
BRANCH_VARIANT = 'Bug'
TARGET_TECHNIQUE = 'DR'
TARGET_METRIC_ABBREV = 'CVT'
TARGET_METRIC_NAME = 'Community Vitality Tracking'
TESTING_TYPE = 'Security White-box Testing'
TECHNIQUE = 'Dependency Risk (SCA)'
METRIC_TOOL_MAP = {
    'hidden_relationship_mapping': {'classification': 'Transitive Dependency Analysis', 'metric': 'Hidden Relationship Mapping', 'tool': 'pip-audit'},
    'legal_risk_validation': {'classification': 'License Compliance Testing', 'metric': 'Legal Risk Validation', 'tool': 'pip-audit'},
    'trust_integrity_verification': {'classification': 'Supply Chain Security Analysis', 'metric': 'Trust Integrity Verification', 'tool': 'pip-audit'},
    'community_vitality_tracking': {'classification': 'Dependency Health Monitoring', 'metric': 'Community Vitality Tracking', 'tool': 'pip-audit'},
    'mitigation_effort_ranking': {'classification': 'Risk Prioritization', 'metric': 'Mitigation Effort Ranking', 'tool': 'pip-audit'},
    'real_time_alerting': {'classification': 'Continuous Dependency Monitoring', 'metric': 'Real-Time Alerting', 'tool': 'pip-audit'},
    'known_cve_count': {'classification': 'Vulnerability Dependency Detection', 'metric': 'Known CVE Count', 'tool': 'pip-audit'},
    'version_lag_assessment': {'classification': 'Outdated Dependency Detection', 'metric': 'Version Lag Assessment', 'tool': 'pip-audit'},
}
