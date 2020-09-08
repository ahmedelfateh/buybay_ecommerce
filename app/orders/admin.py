from django.contrib import admin

from .models import Item, Order, OrderItem, PromoCode

# Register your models here.


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(PromoCode)