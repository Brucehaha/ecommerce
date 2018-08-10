from django.urls import path, re_path
from .views import RetailerListView,create_retailer


app_name="retailers"

urlpatterns = [
    path('', RetailerListView.as_view(), name="list"),
    path('create/', create_retailer, name="create"),
    re_path(r'^edit_retailer/(?P<retailer_pk>\d+)/$', views.edit_question,
    name='edit_question'),
    # re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),

 ]
