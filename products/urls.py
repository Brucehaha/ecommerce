from django.urls import path, re_path
from products.views import (ProductListView,
                            ProductDetailView,
                            )

app_name="products"
urlpatterns = [
    path('', ProductListView.as_view(), name="list"),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),

 ]
