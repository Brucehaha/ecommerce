from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


def login(request):
	form = LoginForm(request.POST or None)
	context = {
		"form": form
	}
	print("User Logged in")
	if form.is_valid():
		print(form.cleaned_data)
		context['form']=LoginForm()
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			print(request.user.is_authenticated)

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
