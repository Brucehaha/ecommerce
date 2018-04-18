from django.shortcuts import render, redirect
from django.urls import reverse 
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


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
	guest_form = GuestForm()
	user = request.user

	if new_cart or cart_obj.products.count() == 0:
		return redirect("carts:cart")
	else:
		pass
		
	billing_profile, new_billing_profile = BillingProfile.objects.new_or_get(request)

	if billing_profile is not None:
		'''check if order is created, if created, retrieve the data, if not, 
		firstly check the deactivate the order with same cart, them create new order based on the same cart'''
		order_obj, oder_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

		##->moved to order manager
		# #forbiden create new order with same cart repeately
		# order_qs =  Order.objects.filter(cart=cart_obj, billing_profile=billing_profile, active=True)
		# if order_qs.count()==1:
		# 	order_obj = order_qs.first()
		# else:
		# 	# get rid of the olde order and create the new order --->the following code has been moved to the order manager
		# 	# older_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
		# 	# if older_order_qs.exists():
		# 	# 	older_order_qs.update(active=False)
		# 	order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
		# 	#if customer mak  e a payment after checkout, get rid the old cart, if not paid, load the cart when login again
		# 	if paid is not None:
		# 		cart_obj.active = False
		# 		cart_obj.save()

	context={
		"order_obj" : order_obj,
		"form": form,
		"billing_profile" : billing_profile,
		"guest_form" : guest_form

	}
	return render(request, "carts/checkout.html", context)