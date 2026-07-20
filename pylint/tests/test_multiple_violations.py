"""Test case designed to trigger multiple violations across different severities (Error, Warning, Convention, Refactor, Custom)."""

class badName:  # C0103 (Convention: invalid-name)
    def __init__(self):
        self.X = 1
        
    def perform_action(self):
        # 1. Error: E0602 (undefined-variable)
        y = undefined_variable + 10
        
        # 2. Warning: W0612 (unused-variable)
        dead_data = "test"
        
        # 3. Custom Checker warning: W9901 (avoid-print)
        print("Logging action...")
        
        # 4. Convention: C0301 (line-too-long) - this line exceeds 80 characters limit
        extra_long_variable_representing_style_violation_for_checking_purposes = y
        
        return extra_long_variable_representing_style_violation_for_checking_purposes
