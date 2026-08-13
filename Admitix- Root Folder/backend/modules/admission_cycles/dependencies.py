"""FastAPI dependencies for admission cycles."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
AdmissionCycleDb = Annotated[Session, Depends(get_db)]
