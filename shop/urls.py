from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from shop.views import (
    base_view,
    category_view,
    product_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
    change_item_qty,
    checkout_view,
    order_create_view,
    make_order_view,
    account_view,
    registration_view,
    login_view,
    support_view,
    send_support_view,
)

urlpatterns = [
    path('category/<category_slug>/', category_view, name='category_detail'),
    path('product/<product_slug>/', product_view, name='product_detail'),
    path('add_to_cart/',add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty', change_item_qty, name='change_item_qty'),
    path('cart/',cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('thank_you/', make_order_view, name='thank_you'),
    path('order/', order_create_view, name='create_order'),
    path('account/', account_view, name='account'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    path('support/', support_view, name='support'),
    path('suppor_sended/', send_support_view, name='support_sended'),
    path('', base_view, name='base'),
]