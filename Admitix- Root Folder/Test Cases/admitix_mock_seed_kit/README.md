# Admitix Mock / Seed Data Kit

This seed script is built from the actual backend schemas/models in the
uploaded Admitix backend.

## What it solves

You do NOT manually enter UUIDs.

The backend creates UUIDs. The script captures every returned UUID and uses
it for the next dependent record.

Example:

```text
Institution
   ↓ institution_id returned by API
Faculty
   ↓ faculty_id returned by API
Department
   ↓ department_id
Staff
   ↓ staff_id
Department.hod_staff_id
```

The HOD relationship is deliberately handled in two steps:

1. Department is created without HOD.
2. Staff is created with `department_id`.
3. Department is PATCHed with the returned `staff_id`.

## Start backend first

Example:

```bat
uvicorn app.main:app --reload
```

## Install dependency

If you already have the backend environment with `httpx`, nothing else is
needed. Otherwise:

```bat
pip install httpx
```

## Run

From this folder:

```bat
py seed.py
```

Default backend:

```text
http://127.0.0.1:8000
```

Other backend URL:

```bat
py seed.py --base-url http://127.0.0.1:8000
```

## Optional login

If your development API requires authentication for mutations:

```bat
set ADMITIX_EMAIL=your@email.com
set ADMITIX_PASSWORD=yourpassword
py seed.py
```

Or:

```bat
py seed.py --email your@email.com --password yourpassword
```

## Demo records

The script creates/reuses deterministic demo records including:

- roles
- institution
- faculties
- departments
- staff
- courses
- fee structures
- seat matrix
- document types
- admission cycle
- users
- students
- education details
- entrance exam scores
- applications
- application preferences
- documents
- AI verification
- payments
- notifications
- chat history
- audit log

## Important

The script is intended for a development/test database.

It uses mock values and example.com file URLs. It does not upload real
documents.

It is designed to be re-runnable. It first GETs existing records and reuses
matching deterministic mock records rather than blindly creating duplicates.

## After seeding

Run your API smoke tester again:

```bat
py test_all_apis.py
```

Then open the Admitix frontend and verify the lists/details/dashboard using
the populated data.

## Next phase

After seed data works, the next automated test should separately exercise:

POST → verify response → PATCH → verify response → DELETE

using only records created specifically by the test runner.
