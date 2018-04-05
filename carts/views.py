from django.shortcuts import render
from .models import Cart
from products.models import Product


def cart_page(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render(request, "carts/home.html", {})


def cart_update(request):
	print(request)
	product = Product.objects.get(id=2)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	if cart_obj is not None:
		if product in cart_obj.products.all():
			cart_obj.products.remove(product)
		else:
			cart_obj.products.add(product)
	return render(request, "carts/home.html", {})
