from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import (
						CreateView,
					  	FormView,
						DetailView,
						)
from .forms import LoginForm, RegisterForm, GuestForm
from carts.models import Cart
from .models import GuestEmail
from .signals import user_logged_in
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def account_home_view(request): #accounts/login/?next=/some/path
	return render(request, "accounts/home.html", {})


class AccountHomeView(LoginRequiredMixin, DetailView):
	template_name='home.html'

	def get_object(self):
		return self.request.user
#
# class LoginRequiredMixin(object):
# 	@method_decorator(login_required)
# 	def dispatch(self, *args, **kwargs):
# 		return super(LoginRequiredMixin, self).dispatch(self, *args, **kwargs)

def guest_register(request):
	form = GuestForm(request.POST or None)
	context = {
		"form": form
	}
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		email = form.cleaned_data.get("email")
		new_guest_email = GuestEmail.objects.get_or_create(email=email)
		request.session['guest_email_id'] = email
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			redirect("/register/")
	return redirect("/register/")


class LoginView(FormView):
	form_class = LoginForm
	success_url = '/'
	template_name = 'login.html'

	def form_valid(self, form):
		request = self.request
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, email=email, password=password)
		if user is not None:
			auth_login(request, user)
			user_logged_in.send(user.__class__, instance=user, request=request)
			## retrive the cart and cart items number
			try:
				del request.session['guest_email_id']
			except KeyError:
				pass

			Cart.objects.load_cart(request)
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		return super(LoginView, self).form_invalid(form)



class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'register.html'
	success_url = '/login/'


# def login(request):
# 	form = LoginForm(request.POST or None)
# 	context = {
# 		"form": form
# 	}
#
# 	next_ = request.GET.get('next')
# 	next_post = request.POST.get('next')
# 	redirect_path = next_ or next_post or None
#
# 	if form.is_valid():
# 		username = form.cleaned_data.get("username")
# 		password = form.cleaned_data.get("password")
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			auth_login(request, user)
# 			## retrive the cart and cart items number
# 			try:
# 				del request.session['guest_email_id']
# 			except KeyError:
# 				pass
#
# 			Cart.objects.load_cart(request)
# 			if is_safe_url(redirect_path, request.get_host()):
# 				return redirect(redirect_path)
# 			else:
# 				return redirect("/")
# 		else:
# 			print("Error")
# 	return render(request, "login.html", context)
# # def register(request):
# 	form = RegisterForm(request.POST or None)
# 	context = {
# 		"form": form
# 	}
#
# 	if form.is_valid():
# 		print(form.cleaned_data)
# 		email = form.cleaned_data.get("email")
# 		password = form.cleaned_data.get("password")
#
# 		new_user = User.objects.create_user(email, password)
# 		print(new_user)
# 	return render(request, "register.html", context)
