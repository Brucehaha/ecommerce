from django import forms
from .models import Retailer, SampleBridge,Sample
from itertools import chain
from django.utils.html import conditional_escape
from django.utils.encoding import force_text


# def unique_field_formset(field_name):
#     from django.forms.models import BaseInlineFormSet
#     class UniqueFieldFormSet (BaseInlineFormSet):
#         def clean(self):
#             if any(self.errors):
#             # Don't bother validating the formset unless each form is valid on its own
#                 return
#             values = set()
#             for form in self.forms:
#                 value = form.cleaned_data[field_name]
#                 if value in values:
#                     raise forms.ValidationError('Duplicate values for "%s" are not allowed.' % field_name)
#                 values.add(value)
#     return UniqueFieldFormSet

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

class DeleteForm(forms.Form):
    delete = forms.BooleanField(required=False)
