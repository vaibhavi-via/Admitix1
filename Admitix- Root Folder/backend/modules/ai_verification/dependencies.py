"""FastAPI dependencies for AI verification."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
AIVerificationDb = Annotated[Session, Depends(get_db)]
