from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, CreateView

from django.shortcuts import render, redirect
from .forms import AddressForm
from django.utils.http import is_safe_url
from billing.models import BillingProfile
from .models import Address


class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'addresses/list.html'

    def get_queryset(self):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)

class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = '/addresses'

    def form_valid(self, form):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        instance = form.save(commit=False)
        instance.billing_profile = billing_profile
        instance.save()
        return super(AddressCreateView, self).form_valid(form)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'addresses/update.html'
    form_class = AddressForm
    success_url = '/addresses'
    initial={'address_line1': '13, Olver Street', 'address_line2': None, 'suburb': 'Preston', 'state': 'Victoria', 'country': 'Australia', 'postcode': '3072'}


    def get_queryset(self):
        request = self.request
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        return Address.objects.filter(billing_profile=billing_profile)

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
			else:
				redirect("carts:checkout")
		return redirect("carts:checkout")
