from django.urls import path
from carts.views import cart_page, cart_update, check_out

app_name="carts"
urlpatterns = [
    path('', cart_page, name="cart"),
    path('update', cart_update, name="update"),
    path('update2', cart_update,  {'foo': 'bar'}, name="update2"),
    path('checkout', check_out, name="checkout"),
 ]
