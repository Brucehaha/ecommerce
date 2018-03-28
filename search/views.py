from django.views.generic import ListView 
from django.shortcuts import render, get_object_or_404
from products.models import Product


class SearchProductView(ListView):
	template_name = "search/view.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		method_dic = request.GET 
		print(method_dic)
		query = method_dic.get('q', None) #or method_dic['q']
		print(query)
		if query is not None:
			return Product.objects.filter(title__icontains=query)
		return Product.objects.featured()
