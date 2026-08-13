from common.repository import CRUDRepository
from modules.audit_logs.models import AuditLog


class AuditLogRepository(CRUDRepository[AuditLog]):
    def __init__(self) -> None:
        super().__init__(AuditLog)
