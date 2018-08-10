from django import forms
from django.forms import formset_factory
from .models import Retailer, SampleBridge

class RetailerForm(forms.ModelForm):
    class Meta:
        model = Retailer
        exclude = [
            'is_active',
            'sample'
        ]
    def __init__(self, *args, **kwargs):
        super(RetailerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control input-sm'

class SampleBridgeForm(forms.ModelForm):
    class Meta:
        model = SampleBridge
        fields = [
            'sample',
            'number',
        ]
    def __init__(self, *args, **kwargs):
        super(SampleBridgeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control input-sm'

SampleBridgeFormSet = forms.modelformset_factory(
    SampleBridge,
    form = SampleBridgeForm,
    fields=('sample', 'number'),
    extra=2,
)

SampleBridgeInlineFormSet = forms.inlineformset_factory(
    Retailer,
    SampleBridge,
    formset=SampleBridgeFormSet,
    fields=('sample', 'number'),
    min_num=1,
    extra=2,

)
