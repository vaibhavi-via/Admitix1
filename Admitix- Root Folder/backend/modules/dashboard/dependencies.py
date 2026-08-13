"""FastAPI dependencies for dashboard queries."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
DashboardDb = Annotated[Session, Depends(get_db)]
