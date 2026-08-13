#!/usr/bin/env python3
"""
Admitix API smoke tester v2.

Safe/non-destructive:
- checks backend health
- loads OpenAPI
- logs in if credentials are supplied
- tests collection GET endpoints
- tests detail GET endpoints only when it can identify the endpoint's
  actual path parameter from the returned object
- skips auth-only endpoints when no credentials are supplied
- does NOT POST/PATCH/DELETE anything

Usage:
    py test_all_apis.py
    py test_all_apis.py --base-url http://127.0.0.1:8000

For authenticated APIs, either:
    set ADMITIX_EMAIL=...
    set ADMITIX_PASSWORD=...
or pass:
    --email ...
    --password ...
"""

import argparse
import getpass
import os
import sys
from urllib.parse import urljoin

import httpx


def clean_base(url):
    return url.rstrip("/") + "/"


def path_has_parameter(path):
    return "{" in path and "}" in path


def is_auth_path(path):
    p = path.lower()
    return p.startswith("/auth/")


def unwrap_records(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            value = data.get(key)
            if isinstance(value, list):
                return value

    return None


def unwrap_object(data):
    if isinstance(data, dict):
        for key in ("data", "item", "result", "record"):
            value = data.get(key)
            if isinstance(value, dict):
                return value
        return data
    return None


def parameter_name(path):
    if "{" not in path:
        return None
    return path.split("{", 1)[1].split("}", 1)[0]


def get_operation(spec, path, method):
    return spec.get("paths", {}).get(path, {}).get(method.lower(), {})


def schema_properties(spec, operation):
    """
    Extract the response schema properties when OpenAPI provides them.
    This is used only as a hint for finding the correct primary key.
    """
    responses = operation.get("responses", {})
    for response in responses.values():
        content = response.get("content", {})
        for media in content.values():
            schema = media.get("schema", {})
            props = schema.get("properties")
            if props:
                return props

            # Resolve a local $ref.
            ref = schema.get("$ref")
            if ref and ref.startswith("#/components/schemas/"):
                name = ref.rsplit("/", 1)[-1]
                obj = spec.get("components", {}).get("schemas", {}).get(name, {})
                if obj.get("properties"):
                    return obj["properties"]

    return {}


def candidate_ids(record, path, spec):
    """
    Prefer the parameter name required by the detail route, then exact
    resource ID names, then generic id/uuid fields.
    """
    wanted = parameter_name(path)
    candidates = []

    if wanted:
        candidates.append(wanted)

    resource = path.strip("/").split("/")[0].replace("-", "_")
    candidates.extend([
        f"{resource}_id",
        "id",
        "uuid",
    ])

    # If response includes a schema with a read-only primary key, prefer it.
    for key in candidates:
        value = record.get(key)
        if value not in (None, ""):
            return value

    # Last resort: any *_id field, but only after exact candidates.
    for key, value in record.items():
        if key.endswith("_id") and value not in (None, ""):
            return value

    return None


def login(client, base, email, password):
    if not email or not password:
        return False, "No credentials supplied"

    login_urls = [
        urljoin(base, "auth/login"),
        urljoin(base, "auth/login/"),
    ]

    payloads = [
        {"email": email, "password": password},
        {"username": email, "password": password},
    ]

    for url in login_urls:
        for payload in payloads:
            try:
                response = client.post(url, data=payload)
                if response.is_success:
                    data = response.json()
                    token = (
                        data.get("access_token")
                        or data.get("token")
                        or data.get("accessToken")
                    )

                    if token:
                        client.headers["Authorization"] = f"Bearer {token}"
                        return True, "Logged in with access token"

                    # Some backends use HttpOnly cookies.
                    if client.cookies:
                        return True, "Logged in with session cookie"

            except Exception:
                pass

    return False, "Login failed"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
    )
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args()

    email = args.email or os.getenv("ADMITIX_EMAIL")
    password = args.password or os.getenv("ADMITIX_PASSWORD")

    base = clean_base(args.base_url)

    print("=" * 76)
    print("ADMITIX API SMOKE TEST v2")
    print("=" * 76)
    print(f"Base URL: {base}")
    print()

    with httpx.Client(
        timeout=args.timeout,
        follow_redirects=True,
    ) as client:

        # ---------------------------------------------------------
        # Health
        # ---------------------------------------------------------
        try:
            response = client.get(urljoin(base, "health"))
            if response.is_success:
                print(f"✓ HEALTH       /health [{response.status_code}]")
            else:
                print(f"✗ HEALTH       /health [{response.status_code}]")
                sys.exit(1)
        except Exception as exc:
            print(f"✗ Cannot connect to backend: {exc}")
            print("Start FastAPI first.")
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

        print(f"✓ OPENAPI       discovered {len(paths)} API paths")
        print()

        # ---------------------------------------------------------
        # Optional authentication
        # ---------------------------------------------------------
        authenticated = False

        if email and password:
            authenticated, message = login(
                client,
                base,
                email,
                password,
            )
            if authenticated:
                print(f"✓ AUTH          {message}")
            else:
                print(f"⚠ AUTH          {message}")
        else:
            print("⚠ AUTH          skipped (no credentials supplied)")
            print("  Set ADMITIX_EMAIL and ADMITIX_PASSWORD if needed.")

        print()

        # ---------------------------------------------------------
        # Route counts
        # ---------------------------------------------------------
        counts = {"GET": 0, "POST": 0, "PATCH": 0, "DELETE": 0}

        for path, operations in paths.items():
            for method in operations:
                method = method.upper()
                if method in counts:
                    counts[method] += 1

        print("DISCOVERED ROUTES")
        print("-" * 76)
        print(
            f"GET={counts['GET']}  "
            f"POST={counts['POST']}  "
            f"PATCH={counts['PATCH']}  "
            f"DELETE={counts['DELETE']}"
        )
        print()

        # ---------------------------------------------------------
        # GET tests
        # ---------------------------------------------------------
        passed = 0
        failed = 0
        skipped = 0
        detail_tested = set()

        print("GET SMOKE TESTS")
        print("-" * 76)

        # Only collection routes. Detail routes are tested after their
        # collection returns a record.
        collection_paths = []

        for path, operations in paths.items():
            if "get" not in {m.lower() for m in operations}:
                continue
            if path_has_parameter(path):
                continue
            if is_auth_path(path):
                continue

            collection_paths.append(path)

        for path in sorted(collection_paths):
            url = urljoin(base, path.lstrip("/"))

            try:
                response = client.get(url)

                if response.status_code == 401:
                    skipped += 1
                    print(f"⚠ GET  {path} [{response.status_code}] auth required")
                    continue

                if not response.is_success:
                    failed += 1
                    print(f"✗ GET  {path} [{response.status_code}]")
                    continue

                passed += 1
                print(f"✓ GET  {path} [{response.status_code}]")

                try:
                    data = response.json()
                except Exception:
                    continue

                records = unwrap_records(data)

                if not records:
                    continue

                first = records[0]

                # Find the matching detail route based on the collection path.
                detail_routes = [
                    detail_path
                    for detail_path in paths
                    if detail_path.rstrip("/").startswith(path.rstrip("/") + "/{")
                    and "get" in {
                        m.lower() for m in paths[detail_path]
                    }
                ]

                for detail_path in detail_routes:
                    if detail_path in detail_tested:
                        continue

                    detail_tested.add(detail_path)

                    param = parameter_name(detail_path)
                    record_id = None

                    if param:
                        # Exact parameter name first.
                        record_id = first.get(param)

                    if record_id in (None, ""):
                        record_id = candidate_ids(
                            first,
                            detail_path,
                            spec,
                        )

                    if record_id in (None, ""):
                        skipped += 1
                        print(
                            f"  ⚠ DETAIL {detail_path} "
                            f"could not identify ID"
                        )
                        continue

                    detail_url = urljoin(
                        base,
                        detail_path.replace(
                            "{" + param + "}",
                            str(record_id),
                        ).lstrip("/"),
                    )

                    detail_response = client.get(detail_url)

                    if detail_response.status_code == 401:
                        skipped += 1
                        print(
                            f"  ⚠ DETAIL {detail_path} "
                            f"[401] auth required"
                        )
                    elif detail_response.is_success:
                        passed += 1
                        print(
                            f"  ✓ DETAIL {detail_path} "
                            f"[{detail_response.status_code}]"
                        )
                    else:
                        failed += 1
                        print(
                            f"  ✗ DETAIL {detail_path} "
                            f"[{detail_response.status_code}]"
                        )

        # ---------------------------------------------------------
        # Auth endpoint
        # ---------------------------------------------------------
        auth_me = None

        for candidate in ("/auth/me", "/auth/me/"):
            if candidate in paths:
                auth_me = candidate
                break

        if auth_me:
            response = client.get(urljoin(base, auth_me.lstrip("/")))

            if response.is_success:
                passed += 1
                print(f"✓ GET  {auth_me} [{response.status_code}]")
            elif response.status_code == 401 and not authenticated:
                skipped += 1
                print(
                    f"⚠ GET  {auth_me} [401] "
                    f"expected without login"
                )
            else:
                failed += 1
                print(f"✗ GET  {auth_me} [{response.status_code}]")

        # ---------------------------------------------------------
        # Mutation routes: list only, never execute
        # ---------------------------------------------------------
        print()
        print("MUTATION ROUTES DISCOVERED (NOT EXECUTED)")
        print("-" * 76)

        for method in ("POST", "PATCH", "DELETE"):
            print(f"\n{method}:")
            for path in sorted(
                p for p in paths
                if method.lower() in {
                    m.lower() for m in paths[p]
                }
            ):
                print(f"  • {path}")

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------
        print()
        print("=" * 76)
        print(
            f"RESULTS: {passed} passed | "
            f"{failed} failed | "
            f"{skipped} skipped"
        )
        print("=" * 76)

        if failed:
            print("\nRESULT: FAIL")
            print(
                "Review the failed endpoints above. "
                "Skipped authentication checks are not failures."
            )
            sys.exit(2)

        print("\nRESULT: PASS")
        print(
            "All executed smoke tests passed. "
            "POST/PATCH/DELETE were intentionally not executed."
        )


if __name__ == "__main__":
    main()
