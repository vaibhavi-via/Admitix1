import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

# Existing seeded records. The script only READS these records.
# Replace/add IDs if your seed data changes.
RECORDS = {
    "institutions": "3b449695-a33c-4d6c-a35f-773d960f87a9",
    "roles": "33a4ec04-efd8-4e6a-b30b-a21574bb1529",
}

COLLECTIONS = [
    "/admission-cycles/",
    "/ai-verifications/",
    "/application-preferences/",
    "/application-status-history/",
    "/applications/",
    "/audit-logs/",
    "/chat-history/",
    "/courses/",
    "/departments/",
    "/document-types/",
    "/documents/",
    "/educational-details/",
    "/entrance-exam-scores/",
    "/faculties/",
    "/fee-structure/",
    "/institutions/",
    "/notifications/",
    "/payments/",
    "/roles/",
    "/seat-matrix/",
    "/staff/",
    "/students/",
    "/users/",
]

session = requests.Session()

def clean(path):
    return path.rstrip("/") or "/"

def test_get(path):
    try:
        r = session.get(BASE_URL + path, timeout=TIMEOUT)
        if r.status_code == 200:
            print(f"✓ GET  {path:<35} [{r.status_code}]")
            return True
        print(f"✗ GET  {path:<35} [{r.status_code}]")
        return False
    except requests.RequestException as e:
        print(f"✗ GET  {path:<35} CONNECTION ERROR: {e}")
        return False

def test_get_by_id(collection, record_id):
    path = clean(collection) + "/" + record_id
    try:
        r = session.get(BASE_URL + path, timeout=TIMEOUT)
        if r.status_code == 200:
            print(f"✓ GET  {path:<35} [{r.status_code}]")
            return True
        if r.status_code == 404:
            print(f"↷ GET  {path:<35} [404] no usable seeded record")
            return False
        print(f"✗ GET  {path:<35} [{r.status_code}]")
        return False
    except requests.RequestException as e:
        print(f"✗ GET  {path:<35} CONNECTION ERROR")
        return False

def find_first_id(collection):
    try:
        r = session.get(BASE_URL + collection, timeout=TIMEOUT)
        if r.status_code != 200:
            return None

        data = r.json()

        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = (
                data.get("items")
                or data.get("data")
                or data.get("results")
                or []
            )
        else:
            records = []

        if records and isinstance(records[0], dict):
            return (
                records[0].get("id")
                or records[0].get("uuid")
                or records[0].get("institution_id")
                or records[0].get("role_id")
                or records[0].get("course_id")
            )
    except Exception:
        pass

    return None

def main():
    print()
    print("# ADMITIX SIMPLE CRUD / API TEST")
    print()
    print("Base URL:", BASE_URL)
    print()
    print("This test is READ-ONLY.")
    print("It does NOT create, edit, or delete your mock data.")
    print()

    try:
        r = session.get(BASE_URL + "/health", timeout=TIMEOUT)
        if r.status_code != 200:
            print("✗ Backend health failed:", r.status_code)
            sys.exit(1)
        print("✓ BACKEND HEALTH                 [200]")
    except requests.RequestException as e:
        print("✗ Cannot connect to backend:", e)
        print("Start FastAPI first.")
        sys.exit(1)

    print()
    print("## COLLECTION GET TESTS")
    print()

    passed = 0
    failed = 0

    for path in COLLECTIONS:
        if test_get(path):
            passed += 1
        else:
            failed += 1

    print()
    print("## SEEDED RECORD GET-BY-ID TESTS")
    print()

    # Automatically discover one existing ID from each collection.
    # This avoids inventing relationship IDs.
    for collection in COLLECTIONS:
        record_id = find_first_id(collection)

        if not record_id:
            print(f"↷ GET  {clean(collection)}/<id>: no ID discovered")
            continue

        if test_get_by_id(collection, str(record_id)):
            passed += 1
        else:
            failed += 1

    print()
    print("## RESULT")
    print()
    print(f"✓ Passed : {passed}")
    print(f"✗ Failed : {failed}")
    print()

    if failed == 0:
        print("RESULT: PASS")
        print()
        print("Basic API/CRUD read verification is healthy.")
        sys.exit(0)
    else:
        print("RESULT: REVIEW")
        print()
        print("Failures above are limited to READ operations.")
        print("No database records were modified.")
        sys.exit(1)

if __name__ == "__main__":
    main()