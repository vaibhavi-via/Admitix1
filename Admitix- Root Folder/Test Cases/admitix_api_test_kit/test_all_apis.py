#!/usr/bin/env python3
"""
Admitix API smoke tester.

What it does:
- Reads FastAPI's OpenAPI document from /openapi.json.
- Checks that the API is reachable.
- Tests every GET collection endpoint that requires no path parameters.
- If a collection returns at least one record, automatically tests its detail GET endpoint
  using the first record's UUID/id.
- Reports all discovered POST/PATCH/DELETE endpoints without performing destructive writes.

This is intentionally non-destructive. It is the safe first pass for all 21 modules.
"""

import argparse
import json
import sys
from urllib.parse import urljoin

import httpx


COMMON_ID_FIELDS = (
    "id",
    "uuid",
    "institution_id",
    "faculty_id",
    "department_id",
    "student_id",
    "staff_id",
    "course_id",
    "application_id",
    "preference_id",
    "admission_cycle_id",
    "document_id",
    "document_type_id",
    "education_id",
    "score_id",
    "notification_id",
    "payment_id",
    "role_id",
    "user_id",
    "audit_log_id",
)


def get_id(record):
    if not isinstance(record, dict):
        return None
    for key in COMMON_ID_FIELDS:
        value = record.get(key)
        if value not in (None, ""):
            return value
    for key, value in record.items():
        if key.endswith("_id") and value not in (None, ""):
            return value
    return None


def is_path_parameter(path):
    return "{" in path or "}" in path


def is_collection_path(path):
    return not is_path_parameter(path) and not path.endswith("/health")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Backend base URL, e.g. http://127.0.0.1:8000",
    )
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args()

    base = args.base_url.rstrip("/") + "/"

    with httpx.Client(timeout=args.timeout, follow_redirects=True) as client:
        print("=" * 72)
        print("ADMITIX API SMOKE TEST")
        print("=" * 72)
        print(f"Base URL: {base}")
        print()

        # ---------------------------------------------------------
        # Health
        # ---------------------------------------------------------
        try:
            response = client.get(urljoin(base, "health"))
            if response.is_success:
                print("✓ HEALTH      /health")
            else:
                print(f"✗ HEALTH      /health -> HTTP {response.status_code}")
                sys.exit(1)
        except Exception as exc:
            print(f"✗ Cannot connect to backend: {exc}")
            print("Start FastAPI first, then run this script again.")
            sys.exit(1)

        # ---------------------------------------------------------
        # OpenAPI
        # ---------------------------------------------------------
        try:
            response = client.get(urljoin(base, "openapi.json"))
            response.raise_for_status()
            spec = response.json()
        except Exception as exc:
            print(f"✗ Could not load /openapi.json: {exc}")
            sys.exit(1)

        paths = spec.get("paths", {})

        print(f"✓ OPENAPI      discovered {len(paths)} API paths")
        print()

        counts = {
            "GET": 0,
            "POST": 0,
            "PATCH": 0,
            "DELETE": 0,
        }

        for path, operations in paths.items():
            for method in operations:
                method = method.upper()
                if method in counts:
                    counts[method] += 1

        print("DISCOVERED ROUTES")
        print("-" * 72)
        print(
            f"GET={counts['GET']}  "
            f"POST={counts['POST']}  "
            f"PATCH={counts['PATCH']}  "
            f"DELETE={counts['DELETE']}"
        )
        print()

        # ---------------------------------------------------------
        # Non-destructive GET tests
        # ---------------------------------------------------------
        collection_paths = sorted(
            path
            for path in paths
            if "get" in {m.lower() for m in paths[path]}
            and is_collection_path(path)
        )

        passed = 0
        failed = 0
        tested = 0

        print("GET SMOKE TESTS")
        print("-" * 72)

        for path in collection_paths:
            tested += 1
            url = urljoin(base, path.lstrip("/"))

            try:
                response = client.get(url)

                if response.is_success:
                    passed += 1
                    print(f"✓ GET  {path}  [{response.status_code}]")

                    # Try to test detail GET automatically.
                    try:
                        data = response.json()
                    except Exception:
                        continue

                    records = data if isinstance(data, list) else None

                    # Some APIs wrap lists in {"data": [...]}.
                    if records is None and isinstance(data, dict):
                        for key in ("data", "items", "results"):
                            if isinstance(data.get(key), list):
                                records = data[key]
                                break

                    if records:
                        record_id = get_id(records[0])

                        if record_id is not None:
                            detail_path = path.rstrip("/") + "/" + str(record_id)

                            # Only test it if OpenAPI exposes a matching path.
                            detail_template = path.rstrip("/") + "/{"
                            matching = [
                                p for p in paths
                                if p.startswith(detail_template)
                                and "get" in {
                                    m.lower() for m in paths[p]
                                }
                            ]

                            if matching:
                                detail_url = urljoin(
                                    base,
                                    detail_path.lstrip("/")
                                )
                                detail_response = client.get(detail_url)

                                if detail_response.is_success:
                                    passed += 1
                                    tested += 1
                                    print(
                                        f"  ✓ GET  {detail_path}  "
                                        f"[{detail_response.status_code}]"
                                    )
                                else:
                                    failed += 1
                                    tested += 1
                                    print(
                                        f"  ✗ GET  {detail_path}  "
                                        f"[{detail_response.status_code}]"
                                    )

                else:
                    failed += 1
                    print(f"✗ GET  {path}  [{response.status_code}]")

            except Exception as exc:
                failed += 1
                print(f"✗ GET  {path}  [{type(exc).__name__}: {exc}]")

        print()
        print("MUTATION ROUTES DISCOVERED (NOT EXECUTED)")
        print("-" * 72)

        for method in ("POST", "PATCH", "DELETE"):
            print(f"\n{method}:")
            for path in sorted(
                p for p in paths
                if method.lower() in {
                    m.lower() for m in paths[p]
                }
            ):
                print(f"  • {path}")

        print()
        print("=" * 72)
        print(f"GET TESTS: {passed} passed / {failed} failed / {tested} total")
        print("=" * 72)

        if failed:
            print("\nRESULT: FAIL")
            sys.exit(2)

        print("\nRESULT: PASS")
        print(
            "All tested GET endpoints responded successfully. "
            "POST/PATCH/DELETE routes were discovered but not executed "
            "because they can modify data."
        )


if __name__ == "__main__":
    main()
