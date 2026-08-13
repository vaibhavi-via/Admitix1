"""FastAPI dependencies for courses."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
CourseDb = Annotated[Session, Depends(get_db)]
