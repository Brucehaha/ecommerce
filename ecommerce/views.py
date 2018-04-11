from django.shortcuts import render, redirect

from .forms import ContactForm


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
		"title": "C ontact",
		"content": "Welcome to the home page",
		"form": contact_form,
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	if request.method == "POST":
		print(request.POST)
	return render(request, "contact/view.html", context)

