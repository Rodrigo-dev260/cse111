# Exemple 6
def is_close_enough(actual_value, expected_value, rel):
    # Compute the tolerance.
    tolerance = expected_value * rel
    # Use the tolerance to determinate if actual
    # and expected values are cloase enough to be 
    # consideres equal.
    if abs(actual_value - expected_value) < tolerance:
        return True
    else:
        return False