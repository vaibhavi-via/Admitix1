#!/usr/bin/env python3
"""
Admitix mock/seed data loader.

This script creates realistic demo data through the existing FastAPI API.
UUIDs are NEVER typed manually. IDs returned by the backend are captured
and reused for dependent records.

The script is designed to be re-runnable:
- It searches existing records for the deterministic mock values first.
- If found, it reuses them.
- Otherwise it creates them.

It is intentionally API-based, so this tests the same POST endpoints that
the frontend uses.

Run:
    py seed.py

Optional:
    py seed.py --base-url http://127.0.0.1:8000

If your API requires authentication, provide:
    set ADMITIX_EMAIL=...
    set ADMITIX_PASSWORD=...
    py seed.py

Or:
    py seed.py --email ... --password ...
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from decimal import Decimal
from typing import Any
from urllib.parse import urljoin

import httpx


def base_url(value: str) -> str:
    return value.rstrip("/") + "/"


def list_records(client: httpx.Client, base: str, endpoint: str) -> list[dict]:
    response = client.get(urljoin(base, endpoint.lstrip("/")))
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("data", "items", "results", "records"):
            if isinstance(data.get(key), list):
                return data[key]

    raise RuntimeError(
        f"Unexpected GET response from {endpoint}: {data!r}"
    )


def get_existing(
    client: httpx.Client,
    base: str,
    endpoint: str,
    predicate,
) -> dict | None:
    for record in list_records(client, base, endpoint):
        if predicate(record):
            return record
    return None


def post(
    client: httpx.Client,
    base: str,
    endpoint: str,
    payload: dict,
) -> dict:
    url = urljoin(base, endpoint.lstrip("/"))
    response = client.post(url, json=payload)

    if not response.is_success:
        raise RuntimeError(
            f"POST {endpoint} failed [{response.status_code}]\n"
            f"Payload: {payload}\n"
            f"Response: {response.text}"
        )

    return response.json()


def patch(
    client: httpx.Client,
    base: str,
    endpoint: str,
    payload: dict,
) -> dict:
    url = urljoin(base, endpoint.lstrip("/"))
    response = client.patch(url, json=payload)

    if not response.is_success:
        raise RuntimeError(
            f"PATCH {endpoint} failed [{response.status_code}]\n"
            f"Payload: {payload}\n"
            f"Response: {response.text}"
        )

    return response.json()


def create_or_get(
    client: httpx.Client,
    base: str,
    endpoint: str,
    payload: dict,
    predicate,
    label: str,
) -> dict:
    existing = get_existing(client, base, endpoint, predicate)

    if existing:
        print(f"✓ {label:<28} existing")
        return existing

    created = post(client, base, endpoint, payload)
    print(f"✓ {label:<28} created")
    return created


def login(
    client: httpx.Client,
    base: str,
    email: str | None,
    password: str | None,
    institution_code: str | None,
) -> None:
    if not email or not password:
        print("⚠ Authentication: not supplied; continuing without login")
        return

    payload = {
        "email": email,
        "password": password,
    }

    if institution_code:
        payload["institution_code"] = institution_code

    response = client.post(
        urljoin(base, "auth/login"),
        json=payload,
    )

    if not response.is_success:
        raise RuntimeError(
            f"Login failed [{response.status_code}]\n{response.text}"
        )

    data = response.json()
    token = data.get("access_token")

    if not token:
        raise RuntimeError(
            "Login succeeded but access_token was not returned."
        )

    client.headers["Authorization"] = f"Bearer {token}"
    print("✓ Authentication               logged in")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
    )
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument(
        "--institution-code",
        default="ADM-MOCK-01",
    )
    parser.add_argument("--timeout", type=float, default=20)
    args = parser.parse_args()

    email = args.email or os.getenv("ADMITIX_EMAIL")
    password = args.password or os.getenv("ADMITIX_PASSWORD")

    base = base_url(args.base_url)

    print("=" * 78)
    print("ADMITIX MOCK / SEED DATA")
    print("=" * 78)
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
            health = client.get(urljoin(base, "health"))
            health.raise_for_status()
            print("✓ Backend                      reachable")
        except Exception as exc:
            print(f"✗ Backend unavailable: {exc}")
            sys.exit(1)

        print()

        # Login is optional. Many current Admitix CRUD routes are public
        # in the development backend.
        login(
            client,
            base,
            email,
            password,
            args.institution_code,
        )

        try:
            # =====================================================
            # 1. ROLES
            # =====================================================
            print("1. ROLES")

            role_student = create_or_get(
                client,
                base,
                "/roles/",
                {
                    "role_name": "student",
                    "description": "Mock student role",
                },
                lambda x: x.get("role_name") == "student",
                "Student role",
            )

            role_faculty = create_or_get(
                client,
                base,
                "/roles/",
                {
                    "role_name": "faculty",
                    "description": "Mock faculty/staff role",
                },
                lambda x: x.get("role_name") == "faculty",
                "Faculty role",
            )

            # =====================================================
            # 2. INSTITUTION
            # =====================================================
            print("\n2. INSTITUTIONS")

            institution = create_or_get(
                client,
                base,
                "/institutions/",
                {
                    "institution_name": "Admitix Demo University",
                    "institution_code": args.institution_code,
                    "email": "demo@admitix.com",
                    "phone": "9876543210",
                    "address": "100 Demo Campus Road",
                    "city": "Pune",
                    "state": "Maharashtra",
                    "country": "India",
                    "logo_url": "https://example.com/admitix-demo-logo.png",
                    "status": True,
                },
                lambda x: x.get("institution_code") == args.institution_code,
                "Demo institution",
            )

            institution_id = institution["institution_id"]

            # =====================================================
            # 3. FACULTIES
            # =====================================================
            print("\n3. FACULTIES")

            faculty_engineering = create_or_get(
                client,
                base,
                "/faculties/",
                {
                    "institution_id": institution_id,
                    "faculty_name": "Faculty of Engineering",
                    "description": "Engineering and technology programs",
                    "status": True,
                },
                lambda x: (
                    x.get("institution_id") == institution_id
                    and x.get("faculty_name") == "Faculty of Engineering"
                ),
                "Engineering faculty",
            )

            faculty_management = create_or_get(
                client,
                base,
                "/faculties/",
                {
                    "institution_id": institution_id,
                    "faculty_name": "Faculty of Management",
                    "description": "Management and business programs",
                    "status": True,
                },
                lambda x: (
                    x.get("institution_id") == institution_id
                    and x.get("faculty_name") == "Faculty of Management"
                ),
                "Management faculty",
            )

            # =====================================================
            # 4. DEPARTMENTS
            # HOD is intentionally omitted on create.
            # =====================================================
            print("\n4. DEPARTMENTS")

            dept_cs = create_or_get(
                client,
                base,
                "/departments/",
                {
                    "faculty_id": faculty_engineering["faculty_id"],
                    "institution_id": institution_id,
                    "department_name": "Computer Science and Engineering",
                    "description": "Computer science and software engineering",
                    "status": True,
                },
                lambda x: (
                    x.get("faculty_id") == faculty_engineering["faculty_id"]
                    and x.get("department_name")
                    == "Computer Science and Engineering"
                ),
                "CSE department",
            )

            dept_mba = create_or_get(
                client,
                base,
                "/departments/",
                {
                    "faculty_id": faculty_management["faculty_id"],
                    "institution_id": institution_id,
                    "department_name": "Business Administration",
                    "description": "Business and management studies",
                    "status": True,
                },
                lambda x: (
                    x.get("faculty_id") == faculty_management["faculty_id"]
                    and x.get("department_name")
                    == "Business Administration"
                ),
                "Business department",
            )

            # =====================================================
            # 5. STAFF USERS
            # =====================================================
            print("\n5. STAFF USERS")

            staff_user = create_or_get(
                client,
                base,
                "/users/",
                {
                    "institution_id": institution_id,
                    "role_id": role_faculty["role_id"],
                    "first_name": "Aarav",
                    "last_name": "Sharma",
                    "email": "aarav.sharma@admitix.com",
                    "phone": "9876500001",
                    "password": "AdmitixDemo@123",
                    "is_active": True,
                },
                lambda x: (
                    x.get("email") == "aarav.sharma@admitix.com"
                    and x.get("institution_id") == institution_id
                ),
                "Staff user",
            )

            staff = create_or_get(
                client,
                base,
                "/staff/",
                {
                    "user_id": staff_user["user_id"],
                    "institution_id": institution_id,
                    "department_id": dept_cs["department_id"],
                    "employee_id": "ADM-DEMO-001",
                    "designation": "Head of Department",
                    "joining_date": "2024-07-01",
                    "status": True,
                },
                lambda x: (
                    x.get("employee_id") == "ADM-DEMO-001"
                    and x.get("institution_id") == institution_id
                ),
                "CSE HOD staff",
            )

            # Now that staff exists, connect it as HOD.
            if dept_cs.get("hod_staff_id") != staff["staff_id"]:
                updated = patch(
                    client,
                    base,
                    f"/departments/{dept_cs['department_id']}",
                    {"hod_staff_id": staff["staff_id"]},
                )
                dept_cs = updated
                print("✓ CSE HOD assignment          updated")
            else:
                print("✓ CSE HOD assignment          already set")

            # =====================================================
            # 6. COURSES
            # =====================================================
            print("\n6. COURSES")

            course_btech = create_or_get(
                client,
                base,
                "/courses/",
                {
                    "department_id": dept_cs["department_id"],
                    "institution_id": institution_id,
                    "course_name": "B.Tech Computer Science",
                    "course_code": "BTECH-CSE-DEMO",
                    "duration_years": 4,
                    "eligibility": "12th Science with Mathematics",
                    "status": True,
                },
                lambda x: x.get("course_code") == "BTECH-CSE-DEMO",
                "B.Tech CSE",
            )

            course_mba = create_or_get(
                client,
                base,
                "/courses/",
                {
                    "department_id": dept_mba["department_id"],
                    "institution_id": institution_id,
                    "course_name": "Master of Business Administration",
                    "course_code": "MBA-DEMO",
                    "duration_years": 2,
                    "eligibility": "Bachelor degree",
                    "status": True,
                },
                lambda x: x.get("course_code") == "MBA-DEMO",
                "MBA",
            )

            # =====================================================
            # 7. FEE STRUCTURE
            # =====================================================
            print("\n7. FEE STRUCTURE")

            fee_btech = create_or_get(
                client,
                base,
                "/fee-structure/",
                {
                    "course_id": course_btech["course_id"],
                    "category": "general",
                    "tuition_fee": "120000.00",
                    "admission_fee": "10000.00",
                    "other_fee": "5000.00",
                    "effective_from": "2026-04-01",
                },
                lambda x: (
                    x.get("course_id") == course_btech["course_id"]
                    and x.get("category") == "general"
                    and str(x.get("effective_from", ""))[:10] == "2026-04-01"
                ),
                "B.Tech fee",
            )

            fee_mba = create_or_get(
                client,
                base,
                "/fee-structure/",
                {
                    "course_id": course_mba["course_id"],
                    "category": "general",
                    "tuition_fee": "90000.00",
                    "admission_fee": "8000.00",
                    "other_fee": "4000.00",
                    "effective_from": "2026-04-01",
                },
                lambda x: (
                    x.get("course_id") == course_mba["course_id"]
                    and x.get("category") == "general"
                    and str(x.get("effective_from", ""))[:10] == "2026-04-01"
                ),
                "MBA fee",
            )

            # =====================================================
            # 8. SEAT MATRIX
            # =====================================================
            print("\n8. SEAT MATRIX")

            seat_btech = create_or_get(
                client,
                base,
                "/seat-matrix/",
                {
                    "course_id": course_btech["course_id"],
                    "category": "general",
                    "total_seats": 60,
                    "filled_seats": 12,
                },
                lambda x: (
                    x.get("course_id") == course_btech["course_id"]
                    and x.get("category") == "general"
                ),
                "B.Tech seats",
            )

            seat_mba = create_or_get(
                client,
                base,
                "/seat-matrix/",
                {
                    "course_id": course_mba["course_id"],
                    "category": "general",
                    "total_seats": 40,
                    "filled_seats": 8,
                },
                lambda x: (
                    x.get("course_id") == course_mba["course_id"]
                    and x.get("category") == "general"
                ),
                "MBA seats",
            )

            # =====================================================
            # 9. DOCUMENT TYPES
            # =====================================================
            print("\n9. DOCUMENT TYPES")

            doc_aadhaar = create_or_get(
                client,
                base,
                "/document-types/",
                {
                    "document_name": "Aadhaar Card",
                    "mandatory": True,
                    "description": "Government identity proof",
                },
                lambda x: x.get("document_name") == "Aadhaar Card",
                "Aadhaar document type",
            )

            doc_marksheet = create_or_get(
                client,
                base,
                "/document-types/",
                {
                    "document_name": "12th Marksheet",
                    "mandatory": True,
                    "description": "Higher secondary marksheet",
                },
                lambda x: x.get("document_name") == "12th Marksheet",
                "Marksheet document type",
            )

            # =====================================================
            # 10. ADMISSION CYCLE
            # =====================================================
            print("\n10. ADMISSION CYCLES")

            cycle = create_or_get(
                client,
                base,
                "/admission-cycles/",
                {
                    "institution_id": institution_id,
                    "academic_year": "2026-27",
                    "application_start": "2026-04-01",
                    "application_end": "2026-09-30",
                    "status": "open",
                },
                lambda x: (
                    x.get("institution_id") == institution_id
                    and x.get("academic_year") == "2026-27"
                ),
                "2026-27 cycle",
            )

            # =====================================================
            # 11. STUDENT USERS
            # =====================================================
            print("\n11. STUDENT USERS")

            student_user_1 = create_or_get(
                client,
                base,
                "/users/",
                {
                    "institution_id": institution_id,
                    "role_id": role_student["role_id"],
                    "first_name": "Priya",
                    "last_name": "Patil",
                    "email": "priya.patil@admitix.com",
                    "phone": "9876500011",
                    "password": "AdmitixDemo@123",
                    "is_active": True,
                },
                lambda x: (
                    x.get("email") == "priya.patil@admitix.com"
                    and x.get("institution_id") == institution_id
                ),
                "Priya user",
            )

            student_user_2 = create_or_get(
                client,
                base,
                "/users/",
                {
                    "institution_id": institution_id,
                    "role_id": role_student["role_id"],
                    "first_name": "Rohan",
                    "last_name": "Kulkarni",
                    "email": "rohan.kulkarni@admitix.com",
                    "phone": "9876500012",
                    "password": "AdmitixDemo@123",
                    "is_active": True,
                },
                lambda x: (
                    x.get("email") == "rohan.kulkarni@admitix.com"
                    and x.get("institution_id") == institution_id
                ),
                "Rohan user",
            )

            # =====================================================
            # 12. STUDENT PROFILES
            # =====================================================
            print("\n12. STUDENTS")

            student_1 = create_or_get(
                client,
                base,
                "/students/",
                {
                    "user_id": student_user_1["user_id"],
                    "institution_id": institution_id,
                    "aadhaar_no": "999900001111",
                    "gender": "female",
                    "dob": "2007-05-12",
                    "blood_group": "B+",
                    "category": "general",
                    "nationality": "Indian",
                    "address": "Demo Student Colony",
                    "city": "Pune",
                    "state": "Maharashtra",
                    "pincode": "411001",
                    "parent_name": "Sunita Patil",
                    "parent_phone": "9876500091",
                    "guardian_email": "sunita.patil@example.com",
                },
                lambda x: x.get("user_id") == student_user_1["user_id"],
                "Priya student",
            )

            student_2 = create_or_get(
                client,
                base,
                "/students/",
                {
                    "user_id": student_user_2["user_id"],
                    "institution_id": institution_id,
                    "aadhaar_no": "999900002222",
                    "gender": "male",
                    "dob": "2006-11-21",
                    "blood_group": "O+",
                    "category": "general",
                    "nationality": "Indian",
                    "address": "Demo Student Colony",
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "pincode": "400001",
                    "parent_name": "Rajesh Kulkarni",
                    "parent_phone": "9876500092",
                    "guardian_email": "rajesh.kulkarni@example.com",
                },
                lambda x: x.get("user_id") == student_user_2["user_id"],
                "Rohan student",
            )

            # =====================================================
            # 13. EDUCATIONAL DETAILS
            # =====================================================
            print("\n13. EDUCATIONAL DETAILS")

            education_1 = create_or_get(
                client,
                base,
                "/educational-details/",
                {
                    "student_id": student_1["student_id"],
                    "qualification": "12th",
                    "board_university": "Maharashtra State Board",
                    "institution_name": "Demo Junior College",
                    "passing_year": 2026,
                    "seat_number": "HSC-DEMO-001",
                    "percentage": "88.50",
                    "cgpa": "8.85",
                },
                lambda x: (
                    x.get("student_id") == student_1["student_id"]
                    and x.get("qualification") == "12th"
                ),
                "Priya education",
            )

            education_2 = create_or_get(
                client,
                base,
                "/educational-details/",
                {
                    "student_id": student_2["student_id"],
                    "qualification": "12th",
                    "board_university": "CBSE",
                    "institution_name": "Demo Senior Secondary School",
                    "passing_year": 2026,
                    "seat_number": "CBSE-DEMO-002",
                    "percentage": "82.25",
                    "cgpa": "8.20",
                },
                lambda x: (
                    x.get("student_id") == student_2["student_id"]
                    and x.get("qualification") == "12th"
                ),
                "Rohan education",
            )

            # =====================================================
            # 14. ENTRANCE EXAM SCORES
            # =====================================================
            print("\n14. ENTRANCE EXAM SCORES")

            score_1 = create_or_get(
                client,
                base,
                "/entrance-exam-scores/",
                {
                    "student_id": student_1["student_id"],
                    "exam_name": "JEE Main",
                    "roll_number": "JEE-DEMO-001",
                    "score": "142.50",
                    "percentile": "94.25",
                    "rank": 12000,
                    "exam_year": 2026,
                },
                lambda x: (
                    x.get("student_id") == student_1["student_id"]
                    and x.get("exam_name") == "JEE Main"
                ),
                "Priya JEE score",
            )

            score_2 = create_or_get(
                client,
                base,
                "/entrance-exam-scores/",
                {
                    "student_id": student_2["student_id"],
                    "exam_name": "JEE Main",
                    "roll_number": "JEE-DEMO-002",
                    "score": "128.00",
                    "percentile": "91.40",
                    "rank": 18000,
                    "exam_year": 2026,
                },
                lambda x: (
                    x.get("student_id") == student_2["student_id"]
                    and x.get("exam_name") == "JEE Main"
                ),
                "Rohan JEE score",
            )

            # =====================================================
            # 15. APPLICATIONS
            # =====================================================
            print("\n15. APPLICATIONS")

            application_1 = create_or_get(
                client,
                base,
                "/applications/",
                {
                    "student_id": student_1["student_id"],
                    "cycle_id": cycle["cycle_id"],
                    "remarks": "Mock application for demo/testing",
                },
                lambda x: (
                    x.get("student_id") == student_1["student_id"]
                    and x.get("cycle_id") == cycle["cycle_id"]
                ),
                "Priya application",
            )

            application_2 = create_or_get(
                client,
                base,
                "/applications/",
                {
                    "student_id": student_2["student_id"],
                    "cycle_id": cycle["cycle_id"],
                    "remarks": "Second mock application for demo/testing",
                },
                lambda x: (
                    x.get("student_id") == student_2["student_id"]
                    and x.get("cycle_id") == cycle["cycle_id"]
                ),
                "Rohan application",
            )

            # =====================================================
            # 16. APPLICATION PREFERENCES
            # =====================================================
            print("\n16. APPLICATION PREFERENCES")

            preference_1 = create_or_get(
                client,
                base,
                "/application-preferences/",
                {
                    "application_id": application_1["application_id"],
                    "course_id": course_btech["course_id"],
                    "preference_no": 1,
                    "status": "pending",
                },
                lambda x: (
                    x.get("application_id") == application_1["application_id"]
                    and x.get("course_id") == course_btech["course_id"]
                ),
                "Priya preference",
            )

            preference_2 = create_or_get(
                client,
                base,
                "/application-preferences/",
                {
                    "application_id": application_2["application_id"],
                    "course_id": course_mba["course_id"],
                    "preference_no": 1,
                    "status": "pending",
                },
                lambda x: (
                    x.get("application_id") == application_2["application_id"]
                    and x.get("course_id") == course_mba["course_id"]
                ),
                "Rohan preference",
            )

            # =====================================================
            # 17. DOCUMENTS
            # =====================================================
            print("\n17. DOCUMENTS")

            document_1 = create_or_get(
                client,
                base,
                "/documents/",
                {
                    "application_id": application_1["application_id"],
                    "document_type_id": doc_aadhaar["document_type_id"],
                    "file_name": "priya-aadhaar-demo.pdf",
                    "file_url": "https://example.com/admitix-demo/priya-aadhaar-demo.pdf",
                    "remarks": "Mock document; no real file uploaded",
                },
                lambda x: (
                    x.get("application_id") == application_1["application_id"]
                    and x.get("document_type_id") == doc_aadhaar["document_type_id"]
                ),
                "Priya Aadhaar document",
            )

            document_2 = create_or_get(
                client,
                base,
                "/documents/",
                {
                    "application_id": application_1["application_id"],
                    "document_type_id": doc_marksheet["document_type_id"],
                    "file_name": "priya-marksheet-demo.pdf",
                    "file_url": "https://example.com/admitix-demo/priya-marksheet-demo.pdf",
                    "remarks": "Mock document; no real file uploaded",
                },
                lambda x: (
                    x.get("application_id") == application_1["application_id"]
                    and x.get("document_type_id") == doc_marksheet["document_type_id"]
                ),
                "Priya marksheet",
            )

            # =====================================================
            # 18. AI VERIFICATION
            # =====================================================
            print("\n18. AI VERIFICATIONS")

            ai_verification = create_or_get(
                client,
                base,
                "/ai-verifications/",
                {
                    "document_id": document_1["document_id"],
                    "ocr_text": "Mock Aadhaar verification text",
                    "confidence_score": "98.50",
                    "blur_score": "2.00",
                    "missing_fields": None,
                    "name_match": True,
                    "status": "passed",
                },
                lambda x: x.get("document_id") == document_1["document_id"],
                "AI document verification",
            )

            # =====================================================
            # 19. PAYMENTS
            # =====================================================
            print("\n19. PAYMENTS")

            payment = create_or_get(
                client,
                base,
                "/payments/",
                {
                    "application_id": application_1["application_id"],
                    "fee_id": fee_btech["fee_id"],
                    "amount_paid": "50000.00",
                    "payment_mode": "upi",
                    "transaction_id": "ADM-DEMO-TXN-0001",
                },
                lambda x: x.get("transaction_id") == "ADM-DEMO-TXN-0001",
                "Demo payment",
            )

            # =====================================================
            # 20. NOTIFICATIONS
            # =====================================================
            print("\n20. NOTIFICATIONS")

            notification = create_or_get(
                client,
                base,
                "/notifications/",
                {
                    "user_id": student_user_1["user_id"],
                    "title": "Application received",
                    "message": "Your Admitix demo application has been received.",
                    "notification_type": "in_app",
                },
                lambda x: (
                    x.get("user_id") == student_user_1["user_id"]
                    and x.get("title") == "Application received"
                ),
                "Student notification",
            )

            # =====================================================
            # 21. CHAT HISTORY
            # =====================================================
            print("\n21. CHAT HISTORY")

            chat = create_or_get(
                client,
                base,
                "/chat-history/",
                {
                    "student_id": student_1["student_id"],
                    "question": "What documents are required for admission?",
                },
                lambda x: (
                    x.get("student_id") == student_1["student_id"]
                    and x.get("question")
                    == "What documents are required for admission?"
                ),
                "Student chat",
            )

            # =====================================================
            # 22. AUDIT LOG
            # Audit logs are append-only and have no DELETE/PATCH.
            # =====================================================
            print("\n22. AUDIT LOG")

            audit = create_or_get(
                client,
                base,
                "/audit-logs/",
                {
                    "user_id": student_user_1["user_id"],
                    "institution_id": institution_id,
                    "action": "SEED",
                    "table_name": "mock_data",
                    "record_id": student_1["student_id"],
                    "ip_address": "127.0.0.1",
                },
                lambda x: (
                    x.get("user_id") == student_user_1["user_id"]
                    and x.get("action") == "SEED"
                    and x.get("table_name") == "mock_data"
                    and x.get("record_id") == student_1["student_id"]
                ),
                "Seed audit log",
            )

            # =====================================================
            # SUMMARY
            # =====================================================
            print()
            print("=" * 78)
            print("SEED COMPLETE")
            print("=" * 78)
            print()
            print("Backend-generated UUIDs used automatically:")
            print(f"  institution_id : {institution_id}")
            print(f"  faculty_id     : {faculty_engineering['faculty_id']}")
            print(f"  department_id  : {dept_cs['department_id']}")
            print(f"  staff_id       : {staff['staff_id']}")
            print(f"  course_id      : {course_btech['course_id']}")
            print(f"  student_id     : {student_1['student_id']}")
            print(f"  cycle_id       : {cycle['cycle_id']}")
            print(f"  application_id : {application_1['application_id']}")
            print()
            print("These IDs came from backend responses; none were manually entered.")
            print()
            print("Demo login accounts:")
            print("  Student: priya.patil@admitix.com")
            print("  Password: AdmitixDemo@123")
            print("  Institution code:", args.institution_code)
            print()
            print("IMPORTANT: These are demo/test records. Do not use real personal data.")

        except KeyboardInterrupt:
            print("\nSeed cancelled.")
            sys.exit(130)
        except Exception as exc:
            print()
            print("=" * 78)
            print("SEED FAILED")
            print("=" * 78)
            print(exc)
            print()
            print(
                "Records created before the failure were not automatically "
                "rolled back because this script uses the API. Re-running "
                "the script will reuse deterministic records where possible."
            )
            sys.exit(2)


if __name__ == "__main__":
    main()

