"""Validation helpers for document-type configuration."""

from modules.document_types.constants import DOCUMENT_NAME_MAX_LENGTH


def validate_document_type_name(name: str) -> str:
    value = name.strip()
    if not value:
        raise ValueError("Document type name is required.")
    if len(value) > DOCUMENT_NAME_MAX_LENGTH:
        raise ValueError(f"Document type name cannot exceed {DOCUMENT_NAME_MAX_LENGTH} characters.")
    return value
