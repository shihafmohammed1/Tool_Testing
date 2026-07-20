"""Test case to trigger code style validation (line length and trailing whitespace)."""

def check_style():
    # Below line has trailing whitespace. We put a space at the end of the comment: 
    # This comment line has trailing whitespace! 
    x = 10
    
    # Below line exceeds 80 characters limit configured in our .pylintrc file.
    very_long_variable_name_that_exceeds_the_standard_eighty_character_limit_value = 100
    
    return x + very_long_variable_name_that_exceeds_the_standard_eighty_character_limit_value
