from typing import Protocol

from payment_service.commons import CustomerData, PaymentData, PaymentResponse


class RecurringPaymentProcessorProtocol(Protocol):
    """Protocol for setting up recurring payments."""

    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
