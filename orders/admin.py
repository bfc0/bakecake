from django.contrib import admin
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

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
    list_display = ("customer", "status", "price", "preferred_date")

    def response_post_save_change(self, request, obj):
        res = super().response_post_save_change(request, obj)
        next_url = request.GET.get("next")
        if url_has_allowed_host_and_scheme(next_url,
                                           allowed_hosts=request.get_host()):
            return redirect(next_url)
        else:
            return res
