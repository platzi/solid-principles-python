from pydantic import BaseModel


class PaymentData(BaseModel):
    amount: int
    source: str
    currency: str = "USD"
