def validate_employee_id(value: str) -> str:
    value = value.strip()
    if not value: raise ValueError("Employee ID is required.")
    return value
