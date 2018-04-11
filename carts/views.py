from django.shortcuts import render, redirect
from django.urls import reverse 
from .models import Cart
from products.models import Product
from orders.models import Order


def cart_page(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render(request, "carts/home.html", {'carts':cart_obj})


def cart_update(request, **kwargs):
	product_id = request.POST.get('product_id')
	product = Product.objects.get(id=product_id)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	if cart_obj is not None:
		if product in cart_obj.products.all():
			cart_obj.products.remove(product)
		else:
			cart_obj.products.add(product) 
	request.session['cart_items'] = cart_obj.products.count()
	if kwargs:
		# return redirect(reverse('products:detail', kwargs={'slug':product.slug}))
		return redirect("carts:cart")
	else:
		return redirect(product.get_absolute_url())


def check_out(request):
	cart_obj, new_cart = Cart.objects.new_or_get(request)
	order_obj = None
	if new_cart or cart_obj.products.count() == 0:
		return redirect("carts:home")
	else: 
		order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
	return render(request, "carts/checkout.html", {"object": order_obj})