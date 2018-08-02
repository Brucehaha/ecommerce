from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from addresses.views import addess_create, address_choose, AddressListView, AddressCreateView, AddressUpdateView
from accounts.views import LoginView, RegisterView, GuestRegisterView
from .views import home_page, contact_page, about_page
from carts.views import cart_refresh
from addresses.views import addess_create, address_choose
from accounts.views import LoginView, RegisterView, GuestRegisterView
from products.views import ProductListView,ProductDetailView
from billing.views import payment_method, payment_method_create
from marketing.views import subscribe, MarketingPreferenceView, MailchimpWebhooView
from orders.views import OrderListView
from analytics.views import SalesView, SalesAjaxView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/',about_page, name='about'),
    path('contact/',contact_page, name='contact'),
    ##accounts app
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('guest/', GuestRegisterView.as_view(), name='guest_register'),

    ##accounts app
    path('account/', include('accounts.urls', namespace='account')),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('accounts/', include("accounts.passwords.urls")),

    ##carts app
    path('cart/', include('carts.urls', namespace='cart')),
    ##products app
    path('products/', include('products.urls', namespace='products')),
    ## search app
    path('search/', include('search.urls', namespace='search')),
    ## address
    path('accounts/address', addess_create, name='address'),
    path('accounts/address_choose', address_choose, name='address_choose'),
    path('api/cart/', cart_refresh, name='cart_refresh'),
    re_path(r'^addresses/$', AddressListView.as_view(), name='addresses'),
    re_path(r'^addresses/create/$', AddressCreateView.as_view(), name='address-create'),
    re_path(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),

    path('payment-method/',payment_method, name='payment_method'),
    path('payment-method/create/',payment_method_create, name='payment_method_create'),

    ##marketing
    path('subscribe/',subscribe, name='subscribe'),
    path('subscription/',MarketingPreferenceView.as_view(), name='subscription'),
    path('webhooks/email/',MailchimpWebhooView.as_view(), name='mailchimpwebhook'),
    path('analytics/sales',SalesView.as_view(), name='sales-report'),
    path('analytics/sales/data/', SalesAjaxView.as_view(), name='sales-analytics-data'),

    ##orders
    path('orders/', include('orders.urls', namespace='orders')),

 ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
