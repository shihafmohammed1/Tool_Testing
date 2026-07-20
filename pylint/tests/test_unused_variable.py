"""Test case to trigger unused variable and unused import/definition warnings."""
import os  # Unused import -> W0611

def process_data(data):
    """Processes input data."""
    dead_data = data * 2  # Triggers W0612 (unused-variable)
    
    result = data + 10
    return result
