from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from django.http import HttpResponse, JsonResponse
from django.utils import  timezone

import datetime


# Create your views here.
class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            return render(request, "400.html", {})
        return super(SalesView, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SalesView, self).get_context_data(**kwargs)
        qs = Order.objects.all()
        context['order_total'] = qs.not_created()
        context['order_total_amount']=context['order_total']
        context['order_paid'] = qs.by_status(status='paid')
        context['order_shipped'] = qs.by_status()
        return context
