from django.contrib import admin
from cakes.models import Visit, CartAddition
from cakes.models import Order as StatsOrder
from .models import Order


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'timestamp')


@admin.register(CartAddition)
class CartAdditionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'timestamp')


@admin.register(StatsOrder)
class StatsOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'timestamp')

    def total_revenue(self):
        return sum(order.total_amount for order in StatsOrder.objects.all())

    total_revenue.short_description = 'Total Revenue'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "status", "price")
