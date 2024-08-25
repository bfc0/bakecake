from yookassa import Payment
from django.conf import settings


def create_payment(order_id, amount):
    payment = Payment.create(
        {
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_RETURN_URL
            },
            "capture": True,
            "description": f"Оплата заказа №{order_id}"
        }
    )
    return payment.id, payment.confirmation.confirmation_url
