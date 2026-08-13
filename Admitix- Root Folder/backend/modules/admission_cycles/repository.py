from common.repository import CRUDRepository
from modules.admission_cycles.models import AdmissionCycle


class AdmissionCycleRepository(CRUDRepository[AdmissionCycle]):
    def __init__(self) -> None:
        super().__init__(AdmissionCycle)
