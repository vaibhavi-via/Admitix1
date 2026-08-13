from common.repository import CRUDRepository
from .models import Staff
class StaffRepository(CRUDRepository[Staff]):
    def __init__(self) -> None: super().__init__(Staff)
