from common.repository import CRUDRepository
from .models import EducationDetail
class EducationDetailRepository(CRUDRepository[EducationDetail]):
    def __init__(self) -> None: super().__init__(EducationDetail)
