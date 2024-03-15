from django.contrib import admin
from OnlyShop.main_app.models import Item, ItemOrder
from OnlyShop.order.models import Order


@admin.register(Item)
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'old_price', 'new_price', 'type', 'label',)


@admin.register(ItemOrder)
# Register your models here.
class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('item',)


@admin.register(Order)
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'start_date', 'created_at')
