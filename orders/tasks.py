from background_task import background
from yookassa import Payment
from .models import Order


@background(schedule=60)  # TODO: switch to webhooks
def check_payment_status(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.payment_id:
            payment = Payment.find_one(order.payment_id)
            if payment.status == 'succeeded':
                order.status = "PAY"
                order.save()
    except Order.DoesNotExist:
        pass
