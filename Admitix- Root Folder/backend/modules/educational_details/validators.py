def validate_qualification(value: str) -> str:
    value = value.strip()
    if not value: raise ValueError("Qualification is required.")
    return value
