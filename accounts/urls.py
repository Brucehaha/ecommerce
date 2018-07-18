from django.urls import path, re_path
from .views import AccountHomeView, AccountEmailActivateView, UserDetailUpdateView

app_name = "account"
urlpatterns = [
    path('', AccountHomeView.as_view() ,name='home'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view() ,name='email-activate'),
    path('email/reactivate/', AccountEmailActivateView.as_view() ,name='email-reactivate'),
    path('user/update/', UserDetailUpdateView.as_view() ,name='user-update'),

]
