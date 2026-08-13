# Admitix API Test Kit v2

Replace the previous `test_all_apis.py` with this version.

## 1. Start the backend

For example:

```bash
uvicorn app.main:app --reload
```

Make sure it is listening on:

```text
http://127.0.0.1:8000
```

## 2. Run

```bash
py test_all_apis.py
```

Or:

```bash
py test_all_apis.py --base-url http://127.0.0.1:8000
```

## Authentication

The tester does not require authentication for the basic public GET smoke test.

If `/auth/me` and other endpoints require login, set credentials before running.

Windows CMD:

```bat
set ADMITIX_EMAIL=your@email.com
set ADMITIX_PASSWORD=yourpassword
py test_all_apis.py
```

PowerShell:

```powershell
$env:ADMITIX_EMAIL="your@email.com"
$env:ADMITIX_PASSWORD="yourpassword"
py test_all_apis.py
```

You can also pass:

```bash
py test_all_apis.py --email your@email.com --password yourpassword
```

## What v2 fixes

The previous tester guessed a generic ID from the first `_id` field in a response.
That caused cases such as:

```text
/departments/<institution-id>
/faculties/<institution-id>
```

which produced 404.

v2 first uses the actual `{parameter_name}` from the detail route, such as:

```text
/departments/{department_id}
```

and therefore looks for:

```text
department_id
```

before falling back to other ID fields.

## Safety

This script DOES NOT:

- create records
- update records
- delete records
- modify your database

It only performs GET requests and optional login.

POST/PATCH/DELETE routes are listed for later testing.

## Next step

Once this smoke test passes, the next script should be a dedicated seed/test script that:

1. creates parent records first
2. captures returned UUIDs
3. injects those UUIDs into child records
4. tests POST
5. tests PATCH
6. tests DELETE only for records created by the script

That is safer and more useful than sending generic random data to all 21 modules.
