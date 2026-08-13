from common.repository import CRUDRepository
from modules.notifications.models import Notification


class NotificationRepository(CRUDRepository[Notification]):
    def __init__(self) -> None:
        super().__init__(Notification)
