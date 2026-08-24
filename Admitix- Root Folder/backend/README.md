# Admitix Backend

FastAPI + PostgreSQL backend.

1. Create the PostgreSQL database and run `docs/final_schema.sql`.
2. Copy `.env.example` to `.env` and enter your own DB password, JWT secret and Groq key.
3. Install `requirements.txt`.
4. Run `uvicorn app.main:app --reload --port 8000`.

Student registration uses an institution code. Protected routes require JWT authentication. Uploaded documents are stored under `uploads/` during local development and AI verification results are persisted to `ai_verifications`.

Never commit `.env`, API keys, passwords or uploaded documents.

## Admission officer activation

1. An administrator creates the admission officer under Staff. The account is created as inactive with no usable password.
2. The officer opens `/staff-register` (or `/activate`), enters their staff email and institution code, and requests an OTP.
3. If SMTP is configured, the OTP is emailed. If SMTP is not configured and `AUTH_OTP_EXPOSE_IN_RESPONSE=true`, the local/demo UI displays the generated OTP.
4. The officer enters the OTP and a new password. The account is activated and access/refresh tokens are issued immediately.
5. Admission officers are redirected to the role-protected Officer Dashboard and can review only applications assigned to their staff account.

Optional SMTP settings are documented in `.env.example`.
