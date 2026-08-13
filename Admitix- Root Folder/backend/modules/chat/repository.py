from common.repository import CRUDRepository
from modules.chat.models import ChatHistory


class ChatHistoryRepository(CRUDRepository[ChatHistory]):
    def __init__(self) -> None:
        super().__init__(ChatHistory)
