from django.shortcuts import render
from .models import CatalogueCake


def serialize_cake(cake):
    return {
        'name': cake.name,
        'event': cake.event if cake.event else '',
        'description': cake.description,
        'price': cake.price,
        'image_url': cake.image.url if cake.image else None,
    }


def catalogue(request):
    cakes = CatalogueCake.objects.all()

    context = {
        'cakes': [serialize_cake(cake) for cake in cakes],
    }
    return render(request, 'catalogue.html', context)
