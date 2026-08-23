# Admitix Backend

FastAPI + PostgreSQL backend.

1. Create the PostgreSQL database and run `docs/final_schema.sql`.
2. Copy `.env.example` to `.env` and enter your own DB password, JWT secret and Groq key.
3. Install `requirements.txt`.
4. Run `uvicorn app.main:app --reload --port 8000`.

Student registration uses an institution code. Protected routes require JWT authentication. Uploaded documents are stored under `uploads/` during local development and AI verification results are persisted to `ai_verifications`.

Never commit `.env`, API keys, passwords or uploaded documents.
