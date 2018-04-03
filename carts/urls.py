from django.urls import path
from carts.views import cart_page

app_name="carts"
urlpatterns = [
    path('', cart_page, name="cart"),


 ]
