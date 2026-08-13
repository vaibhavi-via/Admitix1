from common.repository import CRUDRepository
from modules.courses.models import Course, FeeStructure, SeatMatrix


class CourseRepository(CRUDRepository[Course]):
    def __init__(self) -> None:
        super().__init__(Course)


class FeeStructureRepository(CRUDRepository[FeeStructure]):
    def __init__(self) -> None:
        super().__init__(FeeStructure)


class SeatMatrixRepository(CRUDRepository[SeatMatrix]):
    def __init__(self) -> None:
        super().__init__(SeatMatrix)
