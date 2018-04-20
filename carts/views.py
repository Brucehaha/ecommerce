from django.shortcuts import render, redirect
from django.urls import reverse 
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address


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
	if kwargs:
		# return redirect(reverse('products:detail', kwargs={'slug':product.slug}))
		return redirect("carts:cart")
	else:
		return redirect(product.get_absolute_url())


def check_out(request):
	cart_obj, new_cart = Cart.objects.new_or_get(request)
	order_obj = None
	form = LoginForm()
	address_form = AddressForm()
	guest_form = GuestForm()
	shipping_address_id = request.session.get('shipping_address_id')

	if new_cart or cart_obj.products.count() == 0:
		return redirect("carts:cart")
	else:
		pass

	billing_profile, new_billing_profile = BillingProfile.objects.new_or_get(request)

	if billing_profile is not None:
		order_obj, oder_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

		if shipping_address_id is not None:
			shipping_address_obj = Address.objects.get(id=shipping_address_id)
			order_obj.shipping_address = shipping_address_obj

	context={
		"order_obj" : order_obj,
		"form": form,
		"billing_profile" : billing_profile,
		"guest_form" : guest_form,
		"address_form" : address_form,
		"shipping_address_id" : shipping_address_id

	}
	return render(request, "carts/checkout.html", context)