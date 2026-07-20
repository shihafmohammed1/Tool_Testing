"""Test case to demonstrate False Positive Prevention.

Suppresses pylint warnings using inline comments.
"""

def calculate_average(numbers):
    # Triggers unused-variable, disabled locally
    temp_total = sum(numbers)  # pylint: disable=unused-variable
    
    # Triggers invalid-name, disabled locally
    def Bad_Inner_Func():  # pylint: disable=invalid-name
        return 10
        
    Bad_Inner_Func()
    
    return sum(numbers) / len(numbers) if numbers else 0
