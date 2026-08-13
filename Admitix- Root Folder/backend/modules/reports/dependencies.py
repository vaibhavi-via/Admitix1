"""FastAPI dependencies for reports."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
ReportsDb = Annotated[Session, Depends(get_db)]
