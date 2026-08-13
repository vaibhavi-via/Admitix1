from common.repository import CRUDRepository
from modules.document_types.models import DocumentType


class DocumentTypeRepository(CRUDRepository[DocumentType]):
    def __init__(self) -> None:
        super().__init__(DocumentType)
