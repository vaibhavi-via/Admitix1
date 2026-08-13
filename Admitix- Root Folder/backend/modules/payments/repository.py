from common.repository import CRUDRepository
from modules.payments.models import Payment


class PaymentRepository(CRUDRepository[Payment]):
    def __init__(self) -> None:
        super().__init__(Payment)
