"""FastAPI dependencies for institutions."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
InstitutionDb = Annotated[Session, Depends(get_db)]
