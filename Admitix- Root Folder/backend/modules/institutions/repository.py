from common.repository import CRUDRepository
from modules.institutions.models import Institution


class InstitutionRepository(CRUDRepository[Institution]):
    def __init__(self) -> None:
        super().__init__(Institution)
