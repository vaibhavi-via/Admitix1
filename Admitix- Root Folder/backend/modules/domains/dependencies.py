"""FastAPI dependencies for domains."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
DomainDb = Annotated[Session, Depends(get_db)]
