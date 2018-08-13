from django.urls import path, re_path
from . import views


app_name="retailers"

urlpatterns = [
    re_path(r'^$', views.RetailerListView.as_view(), name="list"),
    re_path(r'^create/$', views.create_retailer, name="create"),
    re_path(r'^edit_retailer/(?P<retailer_pk>\d+)/$', views.edit_retailer, name='edit_retailer'),
    re_path(r'^api/$', views.RemoveRetailer, name='api'),

    # re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),

 ]
