from django.urls import path, re_path
from .views import OrderListView, OrderDetailView

app_name = "orders"
urlpatterns = [
	path('list/', OrderListView.as_view() ,name='list'),
	re_path(r'^detail/(?P<id>[0-9A-Za-z]+)/$', OrderDetailView.as_view() ,name='detail'),
]
