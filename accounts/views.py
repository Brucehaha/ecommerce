from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from carts.models import Cart
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail

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
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = email
		if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
		else:
			redirect("/register/") 
	return redirect("/register/") 




def login(request):
	form = LoginForm(request.POST or None)
	context = {
		"form": form
	}

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	print(next_post)
	redirect_path = next_ or next_post or None 
	print(redirect_path)
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			## retrive the cart and cart items number
			Cart.objects.load_cart(request)
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/") 
		else:
			print("Error")
	return render(request, "login.html", context)

def register(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form": form
	}

	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")

		new_user = User.objects.create_user(username, email, password)
		print(new_user)
	return render(request, "register.html", context)    
