# Admitix API Test Kit

## Purpose

This is a safe first-pass API test for the Admitix backend.

It avoids manually testing all 21 modules one by one.

The script:

1. Checks `/health`.
2. Reads FastAPI `/openapi.json`.
3. Discovers all API routes automatically.
4. Tests every GET collection endpoint that does not require a path ID.
5. When a collection contains a record, it tries the corresponding detail GET.
6. Lists every POST/PATCH/DELETE route so you can see the complete API surface.
7. Does NOT create, edit, or delete database records.

## Install

From the backend virtual environment:

```bash
pip install httpx
```

## Run

Start the backend first.

Example:

```bash
uvicorn app.main:app --reload
```

Then, from this folder:

```bash
python test_all_apis.py
```

If your backend is on another port:

```bash
python test_all_apis.py --base-url http://127.0.0.1:8000
```

## Expected output

You should see something like:

```text
ADMITIX API SMOKE TEST
✓ HEALTH      /health
✓ OPENAPI      discovered ... API paths

GET SMOKE TESTS
✓ GET  /institutions/
✓ GET  /faculties/
✓ GET  /departments/
...

RESULT: PASS
```

## Important

This is the first automated smoke-test layer.

It intentionally does not POST/PATCH/DELETE because those operations need valid request bodies,
foreign-key UUIDs, authentication, and sometimes files.

Once this passes, the next useful step is a seed-data script that creates records in dependency order,
for example:

institution -> faculty -> department -> course -> student -> application

The seed script can capture generated UUIDs automatically, so you do not need to type UUIDs manually.
