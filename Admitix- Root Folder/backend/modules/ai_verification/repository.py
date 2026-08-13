from common.repository import CRUDRepository
from modules.ai_verification.models import AIVerification


class AIVerificationRepository(CRUDRepository[AIVerification]):
    def __init__(self) -> None:
        super().__init__(AIVerification)
