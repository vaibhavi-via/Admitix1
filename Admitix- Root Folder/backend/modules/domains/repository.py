from common.repository import CRUDRepository
from modules.domains.models import Domain


class DomainRepository(CRUDRepository[Domain]):
    def __init__(self) -> None:
        super().__init__(Domain)
