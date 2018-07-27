from django.urls import path
from carts.views import cart_page, cart_update, check_out, success, home


app_name="cart"
urlpatterns = [
    path('', cart_page, name="cart"),
    path('home', home, name="home"),
    path('update', cart_update, name="update"),
    path('checkout', check_out, name="checkout"),
    path('success', success, name="success"),
 ]
