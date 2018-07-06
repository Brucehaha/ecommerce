from django.urls import path, re_path
from .views import AccountHomeView, AccountEmailActivateView

app_name = "account"
urlpatterns = [
    path('', AccountHomeView.as_view() ,name='home'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view() ,name='email-activate'),

]
