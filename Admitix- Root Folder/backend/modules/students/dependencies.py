"""FastAPI dependencies for students."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
StudentDb = Annotated[Session, Depends(get_db)]
