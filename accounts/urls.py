from django.urls import path
from .views import AccountHomeView, AccountEmailActivateView

app_name = "account"
urlpatterns = [
    path('', AccountHomeView.as_view() ,name='home'),
    path('reset/confirm/<token>/', AccountEmailActivateView.as_view() ,name='email-activate'),

]
