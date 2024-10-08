from .payment import PaymentProcessorProtocol
from payment_service.commons import CustomerData, PaymentData, PaymentResponse


class OfflinePaymentProcessor(PaymentProcessorProtocol):
    def process_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Processing offline payment for", customer_data.name)
        return PaymentResponse(
            status="success",
            amount=payment_data.amount,
            transaction_id=None,
            message="Offline payment success",
        )