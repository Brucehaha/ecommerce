from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from addresses.views import addess_create, address_choose
from accounts.views import LoginView, RegisterView, guest_register
from .views import home_page, contact_page, about_page
from carts.views import cart_refresh
from products.views import ProductListView,ProductDetailView
from billing.views import payment_method, payment_method_create
from marketing.views import subscribe, MarketingPreferenceView, MailchimpWebhooView
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/',about_page, name='about'),
    path('contact/',contact_page, name='contact'),
    ##accounts app
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('guest/', guest_register, name='guest_register'),

    ##accounts app
    path('account/', include('accounts.urls', namespace='account')),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('accounts/', include("accounts.passwords.urls")),

    ##carts app
    path('cart/', include('carts.urls', namespace='carts')),
    ##products app
    path('products/', include('products.urls', namespace='products')),
    ## search app
    path('search/', include('search.urls', namespace='search')),
    ## address
    path('accounts/address', addess_create, name='address'),
    path('accounts/address_choose', address_choose, name='address_choose'),
    path('api/cart/', cart_refresh, name='cart_refresh'),

    path('payment-method/',payment_method, name='payment_method'),
    path('payment-method/create/',payment_method_create, name='payment_method_create'),

    ##marketing
    path('subscribe/',subscribe, name='subscribe'),
    path('subscription/',MarketingPreferenceView.as_view(), name='subscription'),
    path('webhooks/email/',MailchimpWebhooView.as_view(), name='mailchimpwebhook'),
 ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
