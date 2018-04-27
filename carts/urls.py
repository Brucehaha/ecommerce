from django.urls import path
from carts.views import cart_page, cart_update, check_out, success


app_name="carts"
urlpatterns = [
    path('', cart_page, name="cart"),
    path('update', cart_update, name="update"),
    path('checkout', check_out, name="checkout"),
    path('success', success, name="success"),
 ]
