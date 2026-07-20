"""Test case to trigger naming convention validation warnings."""

class bad_class_name:  # Triggers C0103 (invalid-name) for class name
    def __init__(self):
        self.Value = 42  # Triggers C0103 (invalid-name) for attribute name

def CamelCaseFunction(arg1):  # Triggers C0103 (invalid-name) for function name
    BadVariableName = arg1  # Triggers C0103 (invalid-name) for variable name
    return BadVariableName
