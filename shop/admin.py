from django.contrib import admin
from shop.models import Category, Brand, Product, CartItem, Cart, Order, Comment


def make_payed(modelAdmin, request, queryset):
    queryset.update(status='Оплачен')


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]


make_payed.short_description = 'Пометить как оплаченные'


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment)