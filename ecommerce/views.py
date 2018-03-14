from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
	context = {
		"title": "hi world",
		"content": "Welcome to the home page"
	}
	if request.user.is_authenticated:
		context['premium_content'] = "yahaaaaaaaaaaa"

	return render(request, "home_page.html", context)

def about_page(request):
	context = {
		"title": "About",
		"content": "Welcome to the home page"
	}
	return render(request, "home_page.html", context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context={	
		"title": "contact",
		"content": "Welcome to the home page",
		"form": contact_form,
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	if request.method == "POST":
		print(request.POST)
	return render(request, "contact/view.html", context)

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

			return redirect("/login") 
		else:
			print("Error")

	return render(request, "auth/login.html", context)

def register(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form": form
	}
	if form.is_valid():
		print(form.cleaned_data)
	return render(request, "auth/register.html", context)


def home_page_old(request):
	html_="""
	<!DOCTYPE html>
	<html lang="en">
	  <head>
	    <!-- Required meta tags -->
	    <meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	    <!-- Bootstrap CSS -->
	    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
	  </head>
	  <body>
	    <h1>Hello, world!</h1>

	    <!-- jQuery first, then Tether, then Bootstrap JS. -->
	    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
	    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
	    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
	  </body>
	</html>
	"""