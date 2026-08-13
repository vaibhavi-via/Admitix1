"""FastAPI dependencies for authentication endpoints."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
AuthDb = Annotated[Session, Depends(get_db)]
