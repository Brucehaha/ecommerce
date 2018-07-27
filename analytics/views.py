from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from django.http import HttpResponse, JsonResponse
from django.utils import  timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.db.models import Count, Sum, Avg
from django.core.cache import cache

import pandas as pd


import datetime
# class SalesAjaxView(View):
#     def get(self,request, *args, **kwargs):
#         data = {}
#         qs = cache.get('qs')
#         d_one_week= timezone.now()-timedelta(weeks=1)
#         d_one_month= timezone.now()-relativedelta(month=1)
#         d_one_year= timezone.now()-timedelta(days=365)
#
#         if qs is None:
#             qs = Order.objects.all().not_created().values('timestamp','total')
#             cache.set('qs', qs, 1800)
# # evaluate queryset, then cache the queryset
#         df = pd.DataFrame.from_records(qs)
#         type = request.GET.get("type")
#         print(type)
#         if type == "1week":
#             df3 = df[(df['timestamp'] > d_one_week)]
#             print(df3)
#         if type == "1month":
#             df3 = df[(df['timestamp'] > d_one_month)]
#         if type == "1year":
#             df3 = df[(df['timestamp'] > d_one_year)]
#         if type == "all":
#             df3 = df
#         df2=df3.set_index('timestamp')
#         df2=df2.groupby(df2.index.date).sum()
#         # data=df2.to_dict(orient='dict')
#         data['labels'] = [x.strftime("%b/%d") for x in df2.index]
#         data['values']=list(df2.total.values)
#         return JsonResponse(data)
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
        # evalutate qs to cache queryset
        [q for q in qs]
        context['order_total'] = qs.not_created().recent()
        context['order_total_amount'] = context['order_total'].aggregate(Sum('total'))
        context['order_paid'] = qs.by_status(status='paid')
        context['order_paid_amount'] = context['order_paid'].aggregate(Sum('total'))
        context['order_shipped'] = qs.by_status()
        context['order_shipped_amount'] = context['order_shipped'].aggregate(Sum('total'))
        return context
