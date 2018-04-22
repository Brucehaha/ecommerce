from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from addresses.views import addess_create, address_choose
from accounts.views import login, register, guest_register
from .views import home_page, contact_page, about_page
from products.views import (ProductListView,
                            product_list_view, 
                            ProductDetailView, 
                            product_detail_view,
                            ProductFeaturedListView,
                            ProductFeaturedDetailView,
                            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/',about_page, name='about'),
    path('contact/',contact_page, name='contact'),
    ##accounts app 
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('guest/', guest_register, name='guest_register'),

    ##carts app 
    path('cart/', include('carts.urls', namespace='carts')),
    ##products app
    path('products/', include('products.urls', namespace='products')),
    ## search app
    path('search/', include('search.urls', namespace='search')),
    ## address 
    path('accounts/address', addess_create, name='address'),
     path('accounts/address_choose', address_choose, name='address_choose'),

 ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)