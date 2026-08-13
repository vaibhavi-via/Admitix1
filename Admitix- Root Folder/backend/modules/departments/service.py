"""Business logic for the `departments` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modules.faculties.models import Faculty
from modules.institutions.models import Institution
from modules.users.models import Staff

from .models import Department
from .schema import DepartmentCreate, DepartmentUpdate


def _validate_relationships(
    db: Session,
    *,
    faculty_id: uuid.UUID,
    institution_id: uuid.UUID,
    hod_staff_id: uuid.UUID | None,
) -> None:
    """Validate UUID relationships before SQLAlchemy reaches the database.

    Pydantic already validates UUID *format*. These checks validate that the
    supplied UUIDs actually exist and that the selected faculty belongs to the
    selected institution. This turns confusing FK/database errors into clear
    API responses.
    """
    faculty = db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()
    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found for the supplied faculty_id.",
        )

    institution = (
        db.query(Institution)
        .filter(Institution.institution_id == institution_id)
        .first()
    )
    if institution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found for the supplied institution_id.",
        )

    if faculty.institution_id != institution_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The selected faculty does not belong to the supplied institution.",
        )

    if hod_staff_id is not None:
        staff = db.query(Staff).filter(Staff.staff_id == hod_staff_id).first()
        if staff is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="HOD staff member not found for the supplied hod_staff_id.",
            )
        if staff.institution_id != institution_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The selected HOD staff member does not belong to the supplied institution.",
            )


def create_department(db: Session, department_data: DepartmentCreate) -> Department:
    """Create a new department within a faculty."""

    _validate_relationships(
        db,
        faculty_id=department_data.faculty_id,
        institution_id=department_data.institution_id,
        hod_staff_id=department_data.hod_staff_id,
    )

    department = Department(**department_data.model_dump())

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_departments(db: Session) -> list[Department]:
    """Return every department."""

    return db.query(Department).order_by(Department.department_name).all()


def get_department_by_id(db: Session, department_id: uuid.UUID) -> Department:
    """Fetch a single department by id or raise 404."""

    department = (
        db.query(Department).filter(Department.department_id == department_id).first()
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found."
        )

    return department


def update_department(
    db: Session, department_id: uuid.UUID, department_data: DepartmentUpdate
) -> Department:
    """Partially update a department."""

    department = get_department_by_id(db, department_id)

    update_data = department_data.model_dump(exclude_unset=True)

    # DepartmentUpdate intentionally does not expose institution_id/faculty_id,
    # so relationship validation is only needed for a newly selected HOD here.
    if "hod_staff_id" in update_data and update_data["hod_staff_id"] is not None:
        staff = (
            db.query(Staff)
            .filter(Staff.staff_id == update_data["hod_staff_id"])
            .first()
        )
        if staff is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="HOD staff member not found for the supplied hod_staff_id.",
            )
        if staff.institution_id != department.institution_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The selected HOD staff member does not belong to the department's institution.",
            )

    for field, value in update_data.items():
        setattr(department, field, value)

    db.commit()
    db.refresh(department)

    return department


def delete_department(db: Session, department_id: uuid.UUID) -> None:
    """Delete a department."""

    department = get_department_by_id(db, department_id)

    db.delete(department)
    db.commit()
