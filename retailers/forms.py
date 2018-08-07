from django import forms
from django.forms import formset_factory
from .model import Retailer, SampleBridge

class RetailerForm(forms.ModelForm):
    class Meta:
        model = Retailer

class SampleBridgeForm(forms.ModelForm):
    class Meta:
        model = SampleBridge


SampleBridgeFormSet = forms.modelformset_factory(
    SampleBridge,
    form = SampleBridgeForm,
    extra=2,
)

SampleBridgeInlineFormSet = forms.inlineformset_factory(
    Retailer,
    SampleBridge,
    extra=2,
    formset=SampleBridgeFormSet,
    min_num=1,
)
