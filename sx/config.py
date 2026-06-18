from __future__ import print_function
"""Runtime configuration for Security White-box Testing / Static Vulnerabilities (SAST)."""
LANGUAGE = 'python'
PYTHON_VERSION = '2.6'
BRANCH_TYPE = 'CC'
BRANCH_VARIANT = 'CC'
TARGET_TECHNIQUE = 'SX'
TARGET_METRIC_ABBREV = 'EPS'
TARGET_METRIC_NAME = 'Entry Point Sanitization'
TESTING_TYPE = 'Security White-box Testing'
TECHNIQUE = 'Static Vulnerabilities (SAST)'
METRIC_TOOL_MAP = {
    'best_practice_compliance': {'classification': 'Secure Coding Validation', 'metric': 'Best Practice Compliance', 'tool': 'Semgrep OSS + Bandit'},
    'entry_point_sanitization': {'classification': 'Input Validation Testing', 'metric': 'Entry Point Sanitization', 'tool': 'Semgrep OSS + Bandit'},
    'sensitive_information_tracking': {'classification': 'Data Flow Security Analysis', 'metric': 'Sensitive Information Tracking', 'tool': 'Semgrep OSS + Bandit'},
    'access_control_verification': {'classification': 'Authentication & Authorization Weakness Detection', 'metric': 'Access Control Verification', 'tool': 'Semgrep OSS + Bandit'},
    'supply_chain_security': {'classification': 'Dependency & Library Vulnerability Detection', 'metric': 'Supply Chain Security', 'tool': 'Semgrep OSS + Bandit'},
    'regulatory_alignment': {'classification': 'Compliance & Security Standard Validation', 'metric': 'Regulatory Alignment', 'tool': 'Semgrep OSS + Bandit'},
    'exploit_surface_identification': {'classification': 'Security Vulnerability Detection', 'metric': 'Exploit Surface Identification', 'tool': 'Semgrep OSS + Bandit'},
}
