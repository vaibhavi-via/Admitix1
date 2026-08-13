"""FastAPI dependencies for audit logs."""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
AuditLogDb = Annotated[Session, Depends(get_db)]
