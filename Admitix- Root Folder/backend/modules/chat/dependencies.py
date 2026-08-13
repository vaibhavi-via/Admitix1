"""FastAPI dependencies for chat history."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
ChatDb = Annotated[Session, Depends(get_db)]
