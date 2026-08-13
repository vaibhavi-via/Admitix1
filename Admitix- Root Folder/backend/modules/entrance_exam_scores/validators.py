def validate_exam_name(value: str) -> str:
    value = value.strip()
    if not value: raise ValueError("Exam name is required.")
    return value
