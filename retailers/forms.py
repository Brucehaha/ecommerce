from django import forms
from .models import Retailer, SampleBridge,Sample
from itertools import chain
from django.utils.html import conditional_escape
from django.utils.encoding import force_text

# class DataList(forms.TextInput):
#     def __init__(self, attrs=None, choices=()):
#         super(DataList, self).__init__(attrs)
#         self.choices = list(choices)
#
#     def render(self, name, value, attrs={}, choices=()):
#         attrs['list'] = u'id_%s_list' % name
#         output = super(DataList, self).render(name, value, attrs)
#         output += u'\n' + self.render_options(name, choices)
#         return output
#
#     def render_options(self, name, choices):
#         output = []
#         output.append(u'<datalist id="id_%s_list" style="display:none">' % name)
#         output.append(u'<select name="%s_select"' % name)
#         for option in chain(self.choices, choices):
#             output.append(u'<option value="%s" />' % conditional_escape(force_text(option)))
#         output.append(u'</select>')
#         output.append(u'</datalist>')
#         return u'\n'.join(output)

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
