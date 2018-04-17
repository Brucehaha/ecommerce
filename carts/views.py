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
	guest_email_id = request.session.get('guest_email_id')
	billing_profile = None
	paid = None

	if new_cart or cart_obj.products.count() == 0:
		return redirect("carts:cart")
	else:
		pass
	if user.is_authenticated:
		billing_profile, new_billingprofile= BillingProfile.objects.get_or_create(user=user, email=user.email)
	elif guest_email_id is not None:
		guest_email_obj, new_guest_email_obj= GuestEmail.objects.get_or_create(email=guest_email_id)
		billing_profile, new_billingprofile = BillingProfile.objects.get_or_create(email=guest_email_obj)
	else:
		pass
	
	if billing_profile is not None:
		order_qs =  Order.objects.filter(cart=cart_obj, billingprofile=billing_profile, active=True)
		if order_qs.count()==1:
			order_obj = order_qs.first()
		else:
			older_order_qs = Order.objects.exclude(billingprofile=billing_profile).filter(cart=cart_obj, active=True)
			if older_order_qs.exists():
				older_order_qs.update(active=False)
			order_obj = Order.objects.create(billingprofile=billing_profile, cart=cart_obj)
			#if customer make a payment after checkout
			if paid is not None:
				cart_obj.active = False
				cart_obj.save()

	context={
		"order_obj" : order_obj,
		"form": form,
		"billing_profile" : billing_profile,
		"guest_form" : guest_form

	}
	return render(request, "carts/checkout.html", context)