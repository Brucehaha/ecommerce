from django.views.generic import ListView, DetailView 
from django.shortcuts import render, get_object_or_404

from .models import Product

class ProductListView(ListView):
	queryset = Product.objects.all()
	templates = "products/product_list.html"


def product_list_view(request):
	queryset = Product.objects.all()
	context  ={
		'object_list':queryset
	}

	return render(request, "products/product_list.html", context)


class ProductDetailView(DetailView):
	#queryset = Product.objects.all()
	model = Product
	templates = "products/product_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		print(context)
		context['abc'] = 123
		return context

def product_detail_view(request, pk=None, *args, **kwargs):
	instance = get_object_or_404(Product, pk=pk)

	context  ={
		'object':instance,
		'abc': 123
	}

	return render(request, "products/product_detail.html", context)