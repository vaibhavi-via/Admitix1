from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
)
from .service import (
    create_course,
    get_courses,
    get_course_by_id,
    update_course,
    delete_course,
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "/",
    response_model=CourseRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_course_route(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
):
    return create_course(db, course_data)


@router.get(
    "/",
    response_model=list[CourseRead],
)
async def get_courses_route(
    db: Session = Depends(get_db),
):
    return get_courses(db)


@router.get(
    "/{course_id}",
    response_model=CourseRead,
)
async def get_course_by_id_route(
    course_id: UUID,
    db: Session = Depends(get_db),
):
    return get_course_by_id(db, course_id)


@router.patch(
    "/{course_id}",
    response_model=CourseRead,
)
async def update_course_route(
    course_id: UUID,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
):
    return update_course(db, course_id, course_data)


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course_route(
    course_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_course(db, course_id)
