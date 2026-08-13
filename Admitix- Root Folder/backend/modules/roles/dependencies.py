"""FastAPI dependencies for roles."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
RoleDb = Annotated[Session, Depends(get_db)]
