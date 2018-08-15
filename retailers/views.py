from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from . import forms
from . import models

def RetailerMap(request):
    return render(request, "retailers/map.html", {})

class RetailerListView(ListView):
    model = models.Retailer
    template_name = "retailers/retailer_list.html"

def RemoveRetailer(request):
    if request.method == 'POST':
        i=0
        for item in request.POST:
            print(item)
            if request.POST.get(item) and i is not 0:
                retailer = models.Retailer.objects.filter(pk=item)
                if retailer.exists():
                    retailer.first().delete()
            i+=1
    return redirect("retailers:list")



def create_retailer(request):
    form_class = forms.RetailerForm
    sample_forms = forms.SampleBridgeFormSet(
        queryset = models.SampleBridge.objects.none()
    )
    form = form_class()
    if request.method == 'POST':
        form = form_class(request.POST)
        sample_forms = forms.SampleBridgeFormSet(
            request.POST,
            queryset = models.SampleBridge.objects.none()
        )

    if form.is_valid() and sample_forms.is_valid():
        retailer = form.save()
        samples = sample_forms.save(commit=False)
        for sample in samples:
            sample.retailer = retailer
            sample.save()
            messages.success(request, "Added Retailer")
            return redirect("retailers:list")
    return render(request, 'retailers/retailer_form.html', {
        'form': form,
        'formset':sample_forms
        })


def create_retailer(request):
    form_class = forms.RetailerForm
    sample_forms = forms.SampleBridgeFormSet(
        queryset = models.SampleBridge.objects.none()
    )
    form = form_class()
    if request.method == 'POST':
        form = form_class(request.POST)
        sample_forms = forms.SampleBridgeFormSet(
            request.POST,
            queryset = models.SampleBridge.objects.none()
        )

    if form.is_valid() and sample_forms.is_valid():
        retailer = form.save()
        samples = sample_forms.save(commit=False)
        for sample in samples:
            sample.retailer = retailer
            sample.save()
            messages.success(request, "Added Retailer")
            return redirect("retailers:list")
    return render(request, 'retailers/retailer_form.html', {
        'form': form,
        'formset':sample_forms
        })


def create_retailer(request):
    form_class = forms.RetailerForm
    sample_forms = forms.SampleBridgeInlineFormSet(
        queryset = models.SampleBridge.objects.none()
    )
    form = form_class()
    if request.method == 'POST':
        form = form_class(request.POST)
        sample_forms = forms.SampleBridgeInlineFormSet(
            request.POST,
            queryset = models.SampleBridge.objects.none()
        )

    if form.is_valid() and sample_forms.is_valid():
        retailer = form.save()
        samples = sample_forms.save(commit=False)
        for sample in samples:
            sample.retailer = retailer
            sample.save()
            messages.success(request, "Added Retailer")
            return redirect("retailers:list")
    return render(request, 'retailers/retailer_form.html', {
        'form': form,
        'formset':sample_forms
        })


def edit_retailer(request, retailer_pk):
    retailer = get_object_or_404(models.Retailer, pk=retailer_pk)
    form_class = forms.RetailerForm

    form = form_class(instance=retailer)
    sample_forms = forms.SampleBridgeInlineFormSet(
        queryset = form.instance.samplebridge_set.all()
    )

    if request.method == 'POST':
        form = form_class(request.POST, instance=retailer)
        sample_forms = forms.SampleBridgeInlineFormSet(
            request.POST,
            queryset =form.instance.samplebridge_set.all()
        )

    if form.is_valid() and sample_forms.is_valid():
        form.save()
        samples = sample_forms.save(commit=False)
        for sample in samples:
            sample.retailer = retailer
            sample.save()
        for sample in sample_forms.deleted_objects:
            answer.delete()
        messages.success(request, "Retailder modified")
        return redirect("retailers:list")
    return render(request, 'retailers/retailer_form.html', {
        'form': form,
        'formset':sample_forms,
        })
