from common.repository import CRUDRepository
from modules.students.models import EducationDetail, EntranceExamScore, Student


class StudentRepository(CRUDRepository[Student]):
    def __init__(self) -> None:
        super().__init__(Student)


class EducationDetailRepository(CRUDRepository[EducationDetail]):
    def __init__(self) -> None:
        super().__init__(EducationDetail)


class EntranceExamScoreRepository(CRUDRepository[EntranceExamScore]):
    def __init__(self) -> None:
        super().__init__(EntranceExamScore)
