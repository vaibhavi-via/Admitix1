"""FastAPI dependencies for document types."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
DocumentTypeDb = Annotated[Session, Depends(get_db)]
