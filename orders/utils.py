import cakes.models as m
from orders.models import Order
from django.contrib.auth.forms import AuthenticationForm


def generate_context(request):

    toppings = m.Topping.objects.all()
    shapes = m.Shape.objects.all()
    berries = m.Berry.object.all()
    decors = m.Decoration.object.all()
    levels = m.Level.object.all()
    toppings = m.Topping.object.all()

    address = email = name = phone = ""
    if request.user.is_authenticated:
        last_order = Order.objects.filter(customer=request.user).last()
        if last_order:
            address = last_order.address
            email = last_order.email
            name = last_order.customer_name
            phone = last_order.phone_number

    form = AuthenticationForm()

    context = {
        "DATA": {
            "Levels": [l.name for l in levels],
            "Forms": [s.name for s in shapes],
            "Toppings": [t.name for t in toppings],
            "Berries": [b.name for b in berries],
            "Decors": [d.name for d in decors],

            "lastorder": {
                "address": address,
                "email": email,
                "name": name,
                "phone": phone,
            },
        },
        "Costs": {
            "Levels": [l.price for l in levels],
            "Forms": [s.price for s in shapes],
            "Toppings": [t.price for t in toppings],
            "Berries": [b.price for b in berries],
            "Decors": [d.price for d in decors],
            "Words": 500,
        },
        "ChosenCakeSpecs": {
            "Levels": 0,
            "Form": 0,
            "Toppings": 0,
            "Berries": 0,
            "Decors": 0,
        },
        "form": form,
    }

    return context
