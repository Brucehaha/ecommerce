from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from carts.models import Cart
from .forms import LoginForm, RegisterForm
from django.utils.http import is_safe_url

def login(request):
	form = LoginForm(request.POST or None)
	context = {
		"form": form
	}

	next_ = request.session.get('next')
	next_post = request.session.get('next')
	redirect_path = next_ or next_post or None 
	if form.is_valid():
		print(form.cleaned_data)
		context['form']=LoginForm()
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			## retrive the cart and cart items number
			Cart.objects.new_or_get(request)
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				redirect("/") 
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
