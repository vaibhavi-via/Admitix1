from common.repository import CRUDRepository
from modules.users.models import Staff, User


class UserRepository(CRUDRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)


class StaffRepository(CRUDRepository[Staff]):
    def __init__(self) -> None:
        super().__init__(Staff)
