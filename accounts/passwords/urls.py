from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('password_change/', auth_views.PasswordChangeView.as_view() ,name='change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view() ,name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view() ,name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetDoneView.as_view() ,name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetConfirmView.as_view() ,name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view() ,name='password_reset_complete'),

]

#
# accounts[name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
