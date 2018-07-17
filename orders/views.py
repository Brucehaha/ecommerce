from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order
from billing.models import BillingProfile

# Create your views here.

class OrderListView(LoginRequiredMixin, ListView):
	template_name = "orders/orders.html"
	ordering = "-timestamp"
	paginate_by = 7

	def get_queryset(self):
		request = self.request
		billing_profile, is_created = BillingProfile.objects.new_or_get(request)
		if not is_created:
			queryset = Order.objects.filter(billing_profile=billing_profile)
		else:
			raise ImproperlyConfigured(
				"%(cls)s is missing a QuerySet. Define "
				"%(cls)s.model, %(cls)s.queryset, or override "
				"%(cls)s.get_queryset()." % {
					'cls': self.__class__.__name__
				}
			)
		ordering = self.get_ordering()
		if ordering:
			if isinstance(ordering, str):
				ordering = (ordering,)
			queryset = queryset.order_by(*ordering)
			return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
	template_name = "orders/order.html"

	def get_object(self, *args, **kwargs):
		request =self.request
		id = self.kwargs.get('id')
		billing_profile, is_created = BillingProfile.objects.new_or_get(request)
		try:
			obj = Order.objects.get(order_id=id, billing_profile=billing_profile)
		except Order.DoesNotExist:
			raise Http404("not found")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			obj = qs.first()
		except:
			raise Http404("Uhhmmm")
		return obj
