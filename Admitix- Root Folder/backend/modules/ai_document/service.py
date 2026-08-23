from __future__ import annotations

import io
import json
import os
from pathlib import Path
from typing import Any

import httpx
import pytesseract

TESSERACT_PATH = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
)

if os.path.isfile(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    
from dotenv import load_dotenv
from PIL import Image

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, role_name
from modules.documents.models import Document
from modules.applications.models import Application
from modules.students.models import Student
from modules.ai_verification.models import AIVerification
from modules.users.models import User
from core.enums import AIVerificationStatus


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

BACKEND_ENV = Path(__file__).resolve().parents[2] / ".env"
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"

load_dotenv(ROOT_ENV, override=False)
load_dotenv(BACKEND_ENV, override=False)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Llama 3.3 70B is TEXT based.
# OCR is therefore performed locally first and the extracted text is
# sent to Llama for structuring, verification and comparison.
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
    # "llama-3.3-70b-versatile",
)

MAX_UPLOAD_BYTES = 12 * 1024 * 1024
MAX_IMAGES_PER_FILE = 5
MAX_CROSS_DOCUMENTS = 5

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg",
    "application/pdf",
}


# ---------------------------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------------------------

def _ensure_api_key() -> None:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Add it to the project .env and restart the backend."
        )


def _parse_json(content: str) -> dict[str, Any]:
    """
    Parse JSON returned by Llama.

    Handles:
    - normal JSON
    - ```json ... ```
    - accidental explanatory text around JSON
    """

    text = (content or "").strip()

    if not text:
        raise RuntimeError("Llama returned an empty response.")

    # Remove markdown fences.
    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

        if text.lower().startswith("json"):
            text = text[4:].lstrip()

    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        # Try extracting the outermost JSON object.
        start = text.find("{")
        end = text.rfind("}")

        if start < 0 or end <= start:
            raise RuntimeError(
                "Llama returned an invalid JSON response."
            )

        try:
            value = json.loads(text[start:end + 1])
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Llama returned an invalid JSON response."
            ) from exc

    if not isinstance(value, dict):
        raise RuntimeError(
            "Llama returned an unexpected response format."
        )

    return value


# ---------------------------------------------------------------------------
# OCR
# ---------------------------------------------------------------------------

def _ocr_image(raw: bytes) -> str:
    """
    Run local Tesseract OCR on an image.

    Llama 3.3 70B does not accept images, so OCR happens before
    the Groq request.
    """

    try:
        image = Image.open(io.BytesIO(raw))
        image = image.convert("RGB")

        # Increase resolution for small admission documents.
        width, height = image.size

        if max(width, height) < 1800:
            scale = 1800 / max(width, height)
            image = image.resize(
                (
                    int(width * scale),
                    int(height * scale),
                ),
                Image.Resampling.LANCZOS,
            )

        text = pytesseract.image_to_string(
            image,
            config="--psm 6",
        )

        return text.strip()

    except Exception as exc:
        raise ValueError(
            "OCR could not process the uploaded image. "
            "Make sure Tesseract OCR is installed."
        ) from exc


def _ocr_pdf(raw: bytes) -> str:
    """
    OCR a PDF.

    First tries to extract existing PDF text.
    If the PDF is scanned/image-based, renders pages and runs Tesseract.
    """

    if fitz is None:
        raise RuntimeError(
            "PDF support requires PyMuPDF. "
            "Install the backend requirements and restart."
        )

    try:
        document = fitz.open(
            stream=raw,
            filetype="pdf",
        )

        if document.page_count == 0:
            raise ValueError(
                "The PDF does not contain any pages."
            )

        pages: list[str] = []

        for index in range(
            min(document.page_count, MAX_IMAGES_PER_FILE)
        ):
            page = document.load_page(index)

            # First try normal PDF text extraction.
            page_text = page.get_text("text").strip()

            if page_text:
                pages.append(
                    f"--- Page {index + 1} ---\n{page_text}"
                )
                continue

            # Scanned PDF: render page and OCR it.
            pixmap = page.get_pixmap(
                matrix=fitz.Matrix(2.0, 2.0),
                alpha=False,
            )

            image_bytes = pixmap.tobytes("png")

            page_ocr = _ocr_image(image_bytes)

            pages.append(
                f"--- Page {index + 1} ---\n{page_ocr}"
            )

        document.close()

        return "\n\n".join(pages).strip()

    except ValueError:
        raise

    except Exception as exc:
        raise ValueError(
            "The PDF could not be read or OCR processed."
        ) from exc


async def _read_upload(
    upload: UploadFile,
) -> tuple[str, str]:
    """
    Read uploaded document and return:

        filename, OCR text
    """

    content_type = (
        upload.content_type or ""
    ).lower()

    if content_type not in ALLOWED_TYPES:
        raise ValueError(
            "Unsupported document type. "
            "Use PDF, JPG, PNG, or WEBP."
        )

    raw = await upload.read()

    if not raw:
        raise ValueError(
            f"{upload.filename or 'The file'} is empty."
        )

    if len(raw) > MAX_UPLOAD_BYTES:
        raise ValueError(
            "Each document must be 12 MB or smaller."
        )

    if content_type == "application/pdf":
        text = _ocr_pdf(raw)
    else:
        text = _ocr_image(raw)

    if not text.strip():
        raise ValueError(
            "No readable text was detected in the document."
        )

    return (
        upload.filename or "document",
        text,
    )


# ---------------------------------------------------------------------------
# Groq / Llama 3.3 70B
# ---------------------------------------------------------------------------

async def _groq_json(
    prompt: str,
    max_tokens: int = 5000,
) -> dict[str, Any]:

    _ensure_api_key()

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an admissions document intelligence "
                    "assistant. Return valid JSON only. "
                    "Do not invent information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.1,
        "max_completion_tokens": max_tokens,
        "response_format": {
            "type": "json_object"
        },
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            response = await client.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
            )

        if response.status_code >= 400:
            try:
                detail = (
                    response.json()
                    .get("error", {})
                    .get("message", response.text)
                )
            except Exception:
                detail = response.text

            raise RuntimeError(
                f"Groq API error "
                f"({response.status_code}): {detail}"
            )

        data = response.json()

        content = (
            data["choices"][0]["message"]["content"]
        )

        return _parse_json(content)

    except httpx.TimeoutException as exc:
        raise RuntimeError(
            "Llama took too long to analyze the document. "
            "Please try again."
        ) from exc

    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Could not connect to Groq. "
            "Check your internet connection and API key."
        ) from exc


# ---------------------------------------------------------------------------
# 1. OCR + structured document extraction
# ---------------------------------------------------------------------------

async def extract_document_data(
    upload: UploadFile,
) -> dict[str, Any]:

    filename, raw_text = await _read_upload(upload)

    prompt = f"""
You are the OCR post-processing and document-data extraction engine
for an admissions management system.

The text below was extracted from a student's document using OCR.

Your job is to:

1. Identify the document type.
2. Correct obvious OCR formatting problems.
3. Extract structured fields.
4. Never invent values.
5. Use null when information is missing or unreadable.
6. Preserve the original OCR text in raw_text.

Return JSON only with this exact high-level shape:

{{
    "document_type": "string",
    "raw_text": "complete OCR text",
    "fields": {{
        "full_name": "string or null",
        "date_of_birth": "string or null",
        "document_number": "string or null",
        "parent_name": "string or null",
        "institution": "string or null",
        "course_or_qualification": "string or null",
        "issue_date": "string or null",
        "expiry_date": "string or null",
        "percentage_or_score": "string or null"
    }},
    "additional_fields": {{}},
    "confidence_score": 0,
    "warnings": []
}}

Confidence must be between 0 and 100.

OCR TEXT:

-------------------------
{raw_text}
-------------------------
"""

    result = await _groq_json(
        prompt,
        max_tokens=5000,
    )

    result["file_name"] = filename

    # Keep the actual OCR result available to the frontend/backend.
    result["ocr_text"] = raw_text

    return result


# ---------------------------------------------------------------------------
# 2. AI document verification
# ---------------------------------------------------------------------------

async def analyze_document(
    upload: UploadFile,
) -> dict[str, Any]:

    filename, raw_text = await _read_upload(upload)

    prompt = f"""
You are an AI document verification assistant
for a university admissions system.

The following text was extracted from a submitted document using OCR.

Assess whether the document appears internally consistent
enough for automated admissions screening.

IMPORTANT:

- You are NOT a forensic certification service.
- Do NOT claim legal authenticity.
- Do NOT claim that a document is definitely genuine.
- Flag uncertainty for human review.
- Do not invent evidence.
- Missing information is not automatically fraud.
- OCR errors should be considered when making decisions.

Return JSON only:

{{
    "file_name": "{filename}",
    "document_type": "string",
    "decision": "passed | manual_review | failed",
    "confidence_score": 0,
    "quality": {{
        "legibility": 0,
        "blur_risk": 0,
        "cropping_risk": 0,
        "tampering_risk": 0
    }},
    "checks": [
        {{
            "name": "string",
            "status": "passed | warning | failed",
            "details": "string"
        }}
    ],
    "extracted_identity": {{
        "full_name": "string or null",
        "date_of_birth": "string or null",
        "document_number": "string or null",
        "institution": "string or null"
    }},
    "issues": [],
    "recommended_action": "string"
}}

Use conservative decisions.

If the OCR text contains inconsistencies,
missing key information, suspicious formatting indicators,
or insufficient evidence, prefer manual_review.

DOCUMENT OCR TEXT:

-------------------------
{raw_text}
-------------------------
"""

    result = await _groq_json(
        prompt,
        max_tokens=5000,
    )

    result["file_name"] = filename

    # Useful for debugging/review.
    result["ocr_text"] = raw_text

    return result


# ---------------------------------------------------------------------------
# 3. Cross-document verification
# ---------------------------------------------------------------------------

async def cross_verify_documents(
    files: list[UploadFile],
) -> dict[str, Any]:

    if not files:
        raise ValueError(
            "At least one document is required."
        )

    if len(files) > MAX_CROSS_DOCUMENTS:
        raise ValueError(
            f"A maximum of {MAX_CROSS_DOCUMENTS} "
            "documents can be compared at once."
        )

    documents: list[dict[str, str]] = []

    for upload in files:

        filename, raw_text = await _read_upload(
            upload
        )

        documents.append(
            {
                "file_name": filename,
                "ocr_text": raw_text,
            }
        )

    document_text = "\n\n".join(
        [
            (
                f"========== DOCUMENT {index + 1} ==========\n"
                f"FILE: {doc['file_name']}\n\n"
                f"{doc['ocr_text']}"
            )
            for index, doc in enumerate(documents)
        ]
    )

    prompt = f"""
You are the cross-document verification engine
for a university admissions system.

You have OCR text from multiple documents belonging
to the same applicant.

Compare identity and academic information across documents.

Important rules:

- Do not determine legal authenticity.
- Compare visible/extracted evidence only.
- Ignore differences caused by case or whitespace.
- Names should be treated as important.
- Dates should be treated as important.
- Document numbers should be treated as important.
- Institution names should be compared carefully.
- Qualifications should be compared carefully.
- Scores and percentages should be compared carefully.
- Missing or unreadable information is NOT a mismatch.
- Do not invent values.
- If OCR quality makes comparison uncertain,
  use manual_review.

Return JSON only:

{{
    "overall_status":
        "consistent | mismatches_found | manual_review",

    "overall_confidence": 0,

    "documents": [
        {{
            "file_name": "string",
            "document_type": "string",
            "extracted": {{
                "full_name": "string or null",
                "date_of_birth": "string or null",
                "parent_name": "string or null",
                "document_number": "string or null",
                "institution": "string or null",
                "course_or_qualification": "string or null",
                "percentage_or_score": "string or null"
            }}
        }}
    ],

    "comparisons": [
        {{
            "field":
                "full_name | date_of_birth | parent_name | institution | course_or_qualification | other",

            "status":
                "match | mismatch | not_available | manual_review",

            "values": [
                {{
                    "file_name": "string",
                    "value": "string or null"
                }}
            ],

            "details": "string"
        }}
    ],

    "critical_mismatches": [],

    "recommendation": "string"
}}

Only report mismatch when the evidence supports it.

DOCUMENTS:

{document_text}
"""

    result = await _groq_json(
        prompt,
        max_tokens=7000,
    )

    result["file_names"] = [
        document["file_name"]
        for document in documents
    ]

    return result


async def analyze_and_persist_document(db: Session, document_id, upload: UploadFile, current_user: User):
    document = db.get(Document, document_id)
    if document is None: raise HTTPException(status_code=404, detail="Document not found.")
    application = db.get(Application, document.application_id); student = db.get(Student, application.student_id) if application else None
    if student is None: raise HTTPException(status_code=404, detail="Document application not found.")
    require_same_institution(current_user, student.institution_id)
    if role_name(current_user) == "student" and student.user_id != current_user.user_id: raise HTTPException(status_code=403, detail="You cannot verify this document.")
    result = await analyze_document(upload)
    decision = result.get('decision','manual_review'); status_value={'passed':AIVerificationStatus.PASSED,'failed':AIVerificationStatus.FAILED}.get(decision,AIVerificationStatus.MANUAL_REVIEW)
    quality=result.get('quality') or {}; blur=quality.get('blur_risk'); blur_score=None if blur is None else max(0,min(100,100-float(blur)))
    identity=result.get('extracted_identity') or {}; extracted=(identity.get('full_name') or '').strip().lower(); expected=f"{student.user.first_name} {student.user.last_name or ''}".strip().lower(); name_match=None if not extracted else (expected in extracted or extracted in expected)
    issues=result.get('issues') or []; missing=', '.join(str(x.get('details',x)) for x in issues if isinstance(x,dict) and x.get('status')=='failed') or None
    record=db.query(AIVerification).filter(AIVerification.document_id==document_id).first()
    if record is None: record=AIVerification(document_id=document_id); db.add(record)
    from datetime import datetime, timezone
    record.ocr_text=result.get('ocr_text'); record.confidence_score=result.get('confidence_score'); record.blur_score=blur_score; record.missing_fields=missing; record.name_match=name_match; record.status=status_value; record.verified_at=datetime.now(timezone.utc)
    db.commit(); db.refresh(record)
    result.update({'persisted':True,'verification_id':str(record.verification_id),'document_id':str(document_id),'saved_status':record.status.value})
    return result
