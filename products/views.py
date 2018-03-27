from django.http import Http404
from django.views.generic import ListView, DetailView 
from django.shortcuts import render, get_object_or_404

from .models import Product


class ProductFeaturedListView(ListView):
	#queryset = Product.objects.all()
	templates = "products/product_list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.features()
# 

class ProductFeaturedDetailView(DetailView):
	queryset = Product.objects.features()
	templates = "products/featured_detail.html"

	# def get_queryeset(self, *args, **kwargs):
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')
	# 	return Product.objects.featured()



class ProductListView(ListView):
	templates = "products/product_list.html"
	paginate_by = 2
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all()


def product_list_view(request):
	queryset = Product.objects.all()
	context  ={
		'object_list':queryset
	}

	return render(request, "products/product_list.html", context)



class ProductDetailView(DetailView):
	queryset  = Product.objects.all()
	templates = "products/product_detail.html"

	# def get_context_data(self, *args, **kwargs):
	# 	context = super().get_context_data(*args, **kwargs)
	# 	# print(context)
	# 	context['abc'] = 123
	# 	return context
	def get_object(self, *args, **kwargs):
		request =self.request
		slug = self.kwargs.get('slug')
		#instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("not found")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active= True)
			instance = qs.first()
		except:
			raise Http404("Uhhmmm")
		return instance



def product_detail_view(request, pk=None, *args, **kwargs):
	#instance = get_object_or_404(Product, pk=pk)
	# try:
	# 	instance = Product.objects.get(id=pk)
	# except Product.DoesNotExist:
	# 	print('no product here')
	# 	raise Http404("Product doesn't exit")
	# except: 
	# 	print("huh?")
	qs = Product.objects.get_by_id(id=pk)
	if qs.exists() and qs.count() == 1:
		instance = qs.first()
	else:
		raise Http404("Product doesn't exist")
	context  ={
		'object':instance,
	}

	return render(request, "products/product_detail.html", context)