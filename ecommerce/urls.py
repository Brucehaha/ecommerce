"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include

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

 ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)