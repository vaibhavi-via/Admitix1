from common.repository import CRUDRepository
from .models import EntranceExamScore
class EntranceExamScoreRepository(CRUDRepository[EntranceExamScore]):
    def __init__(self) -> None: super().__init__(EntranceExamScore)
