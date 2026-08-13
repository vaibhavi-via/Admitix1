from common.repository import CRUDRepository
from modules.faculties.models import Faculty


class FacultyRepository(CRUDRepository[Faculty]):
    def __init__(self) -> None:
        super().__init__(Faculty)
