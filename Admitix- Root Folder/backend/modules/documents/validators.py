"""Validation helpers for uploaded documents."""

from modules.documents.constants import ALLOWED_CONTENT_TYPES, MAX_FILE_SIZE_BYTES


def validate_upload(content_type: str, size_bytes: int) -> None:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Unsupported document content type.")
    if size_bytes <= 0 or size_bytes > MAX_FILE_SIZE_BYTES:
        raise ValueError("Document size must be between 1 byte and 10 MB.")
