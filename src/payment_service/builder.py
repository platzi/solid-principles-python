from dataclasses import dataclass
from typing import Optional, Self

from service import PaymentService
from commons import PaymentData, CustomerData
from loggers import TransactionLogger
from notifiers import NotifierProtocol, EmailNotifier, SMSNotifier
from factory import PaymentProcessorFactory
from processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProcessorProtocol,
    RefundProcessorProtocol,
)
from validators import CustomerValidator, PaymentDataValidator


@dataclass
class PaymentServiceBuilder:
    payment_processor: Optional[PaymentProcessorProtocol] = None
    notifier: Optional[NotifierProtocol] = None
    customer_validator: Optional[CustomerValidator] = None
    payment_validator: Optional[PaymentDataValidator] = None
    logger: Optional[TransactionLogger] = None
    refund_processor: Optional[RefundProcessorProtocol] = None
    recurring_processor: Optional[RecurringPaymentProcessorProtocol] = None

    def set_logger(self) -> Self:
        self.logger = TransactionLogger()
        return self

    def set_payment_validator(self) -> Self:
        self.payment_validator = PaymentDataValidator()
        return self

    def set_customer_validator(self) -> Self:
        self.customer_validator = CustomerValidator()
        return self

    def set_payment_processor(self, payment_data: PaymentData) -> Self:
        self.payment_processor = (
            PaymentProcessorFactory.create_payment_processor(payment_data)
        )
        return self

    def set_notifier(self, customer_data: CustomerData) -> Self:
        if customer_data.contact_info.email:
            self.notifier = EmailNotifier()
            return self
        if customer_data.contact_info.phone:
            self.notifier = SMSNotifier(gateway="MyCustomGateway")
            return self

        raise ValueError("No se puede seleccionar clase de notificación")

    def build(self):
        if not all(
            [
                self.payment_processor,
                self.notifier,
                self.customer_validator,
                self.payment_validator,
                self.logger,
            ]
        ):
            missing = [
                name
                for name, value in [
                    ("payment_processor", self.payment_processor),
                    ("notifier", self.notifier),
                    ("customer_validator", self.customer_validator),
                    ("payment_validator", self.payment_validator),
                    ("logger", self.logger),
                ]
                if value is None
            ]
            raise ValueError(f"Missing dependencies: {missing}")

        return PaymentService(
            payment_processor=self.payment_processor,  # type: ignore
            payment_validator=self.payment_validator,
            customer_validator=self.customer_validator,
            notifier=self.notifier,
            logger=self.logger,
        )
