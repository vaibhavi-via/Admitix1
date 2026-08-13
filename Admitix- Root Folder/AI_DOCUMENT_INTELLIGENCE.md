# Admitix AI Document Intelligence

This addition keeps the existing CRUD modules intact and adds a separate AI workspace backed by Groq.

## Features

1. **OCR & Data Extraction** — upload one PDF/image and extract readable text plus common admission fields.
2. **AI Document Verification** — screen legibility, blur/cropping risk, visible consistency signals and return `passed`, `manual_review`, or `failed`.
3. **Cross-Document Verification** — compare 2–5 documents for identity and academic-field consistency.

## Frontend

Open **Documents → AI Document Intelligence**.

Route: `/ai-document-intelligence`

The existing `/ai-verification` CRUD screens remain unchanged.

## Backend endpoints

- `POST /ai/ocr`
- `POST /ai/document-verification`
- `POST /ai/cross-document-verification`

The AI endpoints use multipart file uploads. The existing Axios client was updated only to let the browser set the multipart boundary automatically.

## Groq configuration

The backend AI service reads `GROQ_API_KEY` from the existing project `.env` as a fallback, so the key does **not** need to be copied into the React/Vite environment.

The default vision model is:

`qwen/qwen3.6-27b`

You can override it with `GROQ_VISION_MODEL` in the environment.

## Dependencies

PDF files are converted to page images before being sent to the Groq vision model, so PyMuPDF was added to the Python requirements.

After replacing/updating the project, install dependencies if needed:

```text
pip install -r requirements.txt
```

Then start the existing backend and frontend exactly as before.

## Important behavior

AI results are intentionally treated as screening results, not legal/forensic proof of authenticity. A `manual_review` result is expected for uncertain or suspicious documents.

No database migration is required for these three AI operations. The existing AI verification CRUD table/API is left intact.
