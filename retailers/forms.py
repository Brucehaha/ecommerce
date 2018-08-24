from django import forms
from .models import Retailer, SampleBridge,Sample
from eflooring.utils import UniqueFieldFormSet



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


retailerFormSet = forms.modelformset_factory(
    Retailer,
    form = RetailerForm,
    fields=('business_name', 'phone_number','email'),
    extra=0,
    can_delete=True,
)



SampleBridgeFormSet = forms.modelformset_factory(
    SampleBridge,
    form = SampleBridgeForm,
    formset=UniqueFieldFormSet,#default BaseModelFormSet
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
