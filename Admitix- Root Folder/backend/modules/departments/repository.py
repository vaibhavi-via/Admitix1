from common.repository import CRUDRepository
from modules.departments.models import Department


class DepartmentRepository(CRUDRepository[Department]):
    def __init__(self) -> None:
        super().__init__(Department)
