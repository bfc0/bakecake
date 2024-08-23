from django.contrib import admin
from .models import (CatalogueCake, CustomCake, Level,
                     Shape, Topping, Berry, Decoration, Event,)

admin.site.register(CatalogueCake)
admin.site.register(CustomCake)
admin.site.register(Level)
admin.site.register(Shape)
admin.site.register(Topping)
admin.site.register(Berry)
admin.site.register(Decoration)
admin.site.register(Event)
