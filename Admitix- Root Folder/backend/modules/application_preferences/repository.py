from common.repository import CRUDRepository
from .models import ApplicationPreference
class ApplicationPreferenceRepository(CRUDRepository[ApplicationPreference]):
    def __init__(self) -> None: super().__init__(ApplicationPreference)
