from .loggers import TransactionLogger
from .notifiers import EmailNotifier
from .processors import StripePaymentProcessor
from .service import PaymentService
from .validators import CustomerValidator, PaymentDataValidator

if __name__ == "__main__":
    stripe_payment_processor = StripePaymentProcessor()
    email_notifier = EmailNotifier()
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    logger = TransactionLogger()
    service = PaymentService(
        payment_processor=stripe_payment_processor,
        notifier=email_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
        logger=logger,
    )
    ...
