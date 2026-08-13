from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from .service import analyze_document, cross_verify_documents, extract_document_data

router = APIRouter(prefix="/ai", tags=["AI Document Intelligence"])


@router.post("/ocr")
async def ocr_document(file: UploadFile = File(...)):
    """Extract OCR text and structured fields from one document."""
    try:
        return await extract_document_data(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/document-verification")
async def verify_document(file: UploadFile = File(...)):
    """Run AI-assisted document integrity/quality verification."""
    try:
        return await analyze_document(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/cross-document-verification")
async def verify_documents(files: list[UploadFile] = File(...)):
    """Extract identity fields from multiple documents and cross-check them."""
    if not files:
        raise HTTPException(status_code=400, detail="Upload at least two documents.")
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Cross-document verification needs at least two documents.")
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="You can compare a maximum of five documents at a time.")

    try:
        return await cross_verify_documents(files)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
