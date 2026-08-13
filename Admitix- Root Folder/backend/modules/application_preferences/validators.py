def validate_preference_number(value: int) -> int:
    if value < 1: raise ValueError("Preference number must be positive.")
    return value
