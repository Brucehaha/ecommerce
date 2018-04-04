from django.shortcuts import render
from .models import Cart


def cart_page(request):
	cart_obj =Cart.objects.new_or_get(request)

	return render(request, "carts/home.html", {})