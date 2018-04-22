from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from .forms import AddressForm
from django.utils.http import is_safe_url
from billing.models import BillingProfile
from .models import Address



def addess_create(request):
	form = AddressForm(request.POST or None)
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None 

	if form.is_valid():
		instance = form.save(commit=False)
		billing_profile, new_billing_profile = BillingProfile.objects.new_or_get(request)
		address_type = request.POST.get('address_type', 'shipping')
		instance.billing_profile = billing_profile
		instance.address_type = address_type
		instance.save()
		request.session['{}_address_id'.format(address_type)] = instance.id
		if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
				print(redirect_path)
		else:
			redirect("carts:checkout") 
	return redirect("carts:checkout") 



def address_choose(request):
	if request.user.is_authenticated:
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None 

		if request.method == "POST":

			address_id		= request.POST.get('address', None)
			address_type 	= request.POST.get('address_type', 'shipping')	
			billing_profile, new_billing_profile = BillingProfile.objects.new_or_get(request)

			if address_id is not None:
				qs = Address.objects.filter(billing_profile=billing_profile, id=address_id)
				if qs.exists():
					request.session[address_type+"_address_id"] = address_id

			if is_safe_url(redirect_path, request.get_host()):
					return redirect(redirect_path)
					print(redirect_path)
			else:
				redirect("carts:checkout") 
		return redirect("carts:checkout") 


