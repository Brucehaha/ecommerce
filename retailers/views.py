from django.shortcuts import render
from .models import Retailer
from django.views.generic import ListView
from .forms import RetailerForm, SampleBridgeForm

class RetailerListView(ListView):
    model = Retailer
    template_name = "retailers/retailer_list.html"


def create_retailer(request):
    form = RetailerForm
