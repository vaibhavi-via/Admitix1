"""FastAPI dependencies for users."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
UserDb = Annotated[Session, Depends(get_db)]
