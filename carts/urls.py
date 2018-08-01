from django.urls import path
from carts.views import cart_page, cart_update, check_out, success,entry_update

app_name="cart"
urlpatterns = [
    path('', cart_page, name="home"),
    path('update', cart_update, name="update"),
    path('checkout', check_out, name="checkout"),
    path('success', success, name="success"),
    path('entry', entry_update, name="entry"),
 ]
