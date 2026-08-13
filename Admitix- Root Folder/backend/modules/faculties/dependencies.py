"""FastAPI dependencies for faculties."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
FacultyDb = Annotated[Session, Depends(get_db)]
