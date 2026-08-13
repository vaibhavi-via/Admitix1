"""FastAPI dependencies for departments."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
DepartmentDb = Annotated[Session, Depends(get_db)]
