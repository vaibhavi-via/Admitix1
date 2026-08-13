from common.repository import CRUDRepository
from modules.documents.models import Document


class DocumentRepository(CRUDRepository[Document]):
    def __init__(self) -> None:
        super().__init__(Document)
