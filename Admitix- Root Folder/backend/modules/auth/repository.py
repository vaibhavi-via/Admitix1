from sqlalchemy import select
from sqlalchemy.orm import Session

from common.repository import CRUDRepository
from modules.users.models import User


class AuthRepository(CRUDRepository[User]):
    """Account lookups used by authentication workflows."""

    def __init__(self) -> None:
        super().__init__(User)

    def get_by_email(self, db: Session, email: str, institution_id: object | None = None) -> User | None:
        query = select(User).where(User.email == email)
        query = query.where(User.institution_id == institution_id) if institution_id else query
        return db.scalar(query)
