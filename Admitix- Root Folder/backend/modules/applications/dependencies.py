"""FastAPI dependencies for applications."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
ApplicationDb = Annotated[Session, Depends(get_db)]
