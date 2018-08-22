
from django.utils.http import is_safe_url
from django import forms
from django.contrib import messages



class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "/"
    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
                return redirect_path
        return self.default_next

'''inherit form BaseModelFormSet
 for clean the dupliated model formset values
 like:
 SampleBridgeFormSet = forms.modelformset_factory(
     SampleBridge,
     form = SampleBridgeForm,
     formset=UniqueFieldFormSet,#default BaseModelFormSet
     fields=('sample', 'number'),
     extra=2,
 )'''

class UniqueFieldFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.request =  kwargs.pop('request', None)
        # get field value from view modelformset_factory(field_value='sample',
        #)
        self.field_value=kwargs.pop('field_value', None)

        super(UniqueFieldFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        super(UniqueFieldFormSet, self).clean()
        values = set()
        field_value = self.field_value
        # to get the form.instance.field function
        func = getattr(self, 'form.instance.{}'.format(field_value),"none")
        for form in self.forms:
            #to skip the empty form coz there's extra form for
            # modelformset_factory
            try:
                value = form.cleaned_data[field_value]
            except KeyError:
                break
            form.cleaned_data[field_value] = value
            func = value
            if value in values:
                messages.success(self.request, 'duplicated "%s"' % value)
                raise forms.ValidationError('Duplicate values for "%s" are not allowed.' % value)
            values.add(value)
