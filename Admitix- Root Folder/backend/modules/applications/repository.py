from common.repository import CRUDRepository
from modules.applications.models import Application, ApplicationPreference, ApplicationStatusHistory


class ApplicationRepository(CRUDRepository[Application]):
    def __init__(self) -> None:
        super().__init__(Application)


class ApplicationPreferenceRepository(CRUDRepository[ApplicationPreference]):
    def __init__(self) -> None:
        super().__init__(ApplicationPreference)


class ApplicationStatusHistoryRepository(CRUDRepository[ApplicationStatusHistory]):
    def __init__(self) -> None:
        super().__init__(ApplicationStatusHistory)
