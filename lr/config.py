from __future__ import print_function
"""Runtime configuration for Static Code Analysis / Lint / Rule Violations."""
LANGUAGE = 'python'
PYTHON_VERSION = '2.6'
BRANCH_TYPE = 'Bug'
BRANCH_VARIANT = 'Bug'
TARGET_TECHNIQUE = 'LR'
TARGET_METRIC_ABBREV = 'PSE'
TARGET_METRIC_NAME = 'Project-Specific Enforcement'
TESTING_TYPE = 'Static Code Analysis'
TECHNIQUE = 'Lint / Rule Violations'
METRIC_TOOL_MAP = {
    'violation_density_per_kloc': {'classification': 'Rule Detection Test', 'metric': 'Violation Density per KLOC', 'tool': 'pylint'},
    'resource_waste_identification': {'classification': 'Unused Variable Detection', 'metric': 'Resource Waste Identification', 'tool': 'pylint'},
    'semantic_consistency_score': {'classification': 'Naming Convention Validation', 'metric': 'Semantic Consistency Score', 'tool': 'pylint'},
    'syntactic_uniformity_score': {'classification': 'Code Style Rule Validation', 'metric': 'Syntactic Uniformity Score', 'tool': 'pylint'},
    'structural_threshold_monitoring': {'classification': 'Complexity Rule Detection', 'metric': 'Structural Threshold Monitoring', 'tool': 'pylint'},
    'impact_prioritization': {'classification': 'Rule Severity Classification', 'metric': 'Impact Prioritization', 'tool': 'pylint'},
    'aggregated_risk_assessment': {'classification': 'Multiple Violations Detection', 'metric': 'Aggregated Risk Assessment', 'tool': 'pylint'},
    'accuracy_tuning': {'classification': 'False Positive Prevention', 'metric': 'Accuracy Tuning', 'tool': 'pylint'},
    'project_specific_enforcement': {'classification': 'Custom Rule Validation', 'metric': 'Project-Specific Enforcement', 'tool': 'pylint'},
    'environment_standardization': {'classification': 'Configuration File Handling', 'metric': 'Environment Standardization', 'tool': 'pylint'},
    'automated_gatekeeping': {'classification': 'CI/CD Integration Validation', 'metric': 'Automated Gatekeeping', 'tool': 'pylint'},
    'quality_audit_trail': {'classification': 'Violation Reporting Validation', 'metric': 'Quality Audit Trail', 'tool': 'pylint'},
}
