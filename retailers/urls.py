from django.urls import path, re_path
from .views import RetailerListView

app_name="retailers"

urlpatterns = [
    path('', RetailerListView.as_view(), name="list"),
    # re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),

 ]
