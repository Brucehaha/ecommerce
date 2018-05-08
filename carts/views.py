from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address


def cart_refresh(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = cart_obj.products.all()
	products_array = [{"url":x.get_absolute_url(), "name":x.title, "price":x.price, "id":x.id} for x in products]
	return JsonResponse({"products": products_array,"subtotal":cart_obj.subtotal, "total":cart_obj.total})


def cart_page(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render(request, "carts/home.html", {'carts':cart_obj})


def cart_update(request):
	product_id = request.POST.get('product_id')
	product = Product.objects.get(id=product_id)
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	if cart_obj is not None:
		if product in cart_obj.products.all():
			cart_obj.products.remove(product)
			added = False
		else:
			cart_obj.products.add(product)
			added = True

		request.session['cart_items'] = cart_obj.products.count()
		if request.is_ajax():
			json_data = {
				"added": added,
				"removed": not added,
				"itemCount": cart_obj.products.count(),
			}
			return JsonResponse(json_data)
		return redirect("carts:cart")


def check_out(request):
	cart_obj, new_cart = Cart.objects.new_or_get(request)
	order_obj = None
	form = LoginForm()
	address_form = AddressForm()
	guest_form = GuestForm()
	shipping_address_id = request.session.get('shipping_address_id')
	billing_address_id = request.session.get('billing_address_id')
	address_qs = None

	if new_cart or cart_obj.products.count() == 0:
		return redirect("carts:cart")
	else:
		pass

	billing_profile, new_billing_profile = BillingProfile.objects.new_or_get(request)

	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		order_obj, oder_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

		if shipping_address_id is not None:
			shipping_address_obj = Address.objects.get(id=shipping_address_id)
			order_obj.shipping_address = shipping_address_obj
			del request.session['shipping_address_id']

		if billing_address_id is not None:
			print(billing_address_id)
			billing_address_obj = Address.objects.get(id=billing_address_id)
			order_obj.billing_address = billing_address_obj
			del request.session['billing_address_id']
		if billing_address_id or shipping_address_id:
			order_obj.save()
		'''
		update order_obj to done, "paid"
		del request.session['card_id']
		redirect "success"
		'''
	if request.method == "POST":
		is_done = order_obj.check_done()
		if is_done:
			order_obj.mark_paid()
			cart_obj.cart_checkout()
			try:
				del request.session['cart_id']
				del request.session['cart_items']
				del request.session['guest_email_id']
			except KeyError:
				pass
			return redirect("carts:success")

	context={
		"order_obj" : order_obj,
		"form": form,
		"billing_profile" : billing_profile,
		"guest_form" : guest_form,
		"address_form" : address_form,
		"address_qs" : address_qs,

	}
	return render(request, "carts/checkout.html", context)




def success(request):
	return render(request, "carts/success.html")
