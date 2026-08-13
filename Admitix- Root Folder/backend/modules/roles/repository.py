from common.repository import CRUDRepository
from modules.roles.models import Role


class RoleRepository(CRUDRepository[Role]):
    def __init__(self) -> None:
        super().__init__(Role)
