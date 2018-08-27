import random
import string
from django import forms
from django.contrib import messages
##slugify separete word with dash
from django.utils.text import slugify


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
                continue
            form.cleaned_data[field_value] = value
            func = value
            if value in values:
                messages.success(self.request, 'duplicated "%s"' % value)
                raise forms.ValidationError('Duplicate values for "%s" are not allowed.' % value)
            values.add(value)

def random_string_generator(size=10, chars=(string.ascii_lowercase + string.digits)):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_key_id(instance):
	size = random.randint(30, 45)
	key = random_string_generator(size=size)
	klass = instance.__class__
	qs = klass.objects.filter(key=key)
	if qs:
		return unique_order_id(instance)
	return key

def unique_order_id(instance):
	order_id = random_string_generator(10).upper()
	klass = instance.__class__
	qs = klass.objects.filter(order_id=order_id)
	if qs:
		return unique_order_id(instance)
	return order_id


def unique_slug_generator(instance, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title)

	klass = instance.__class__
	qs = klass.objects.filter(slug=slug)
	if qs:
		new_slug = "{slug}-{randstr}".format(
				slug=slug,
				randstr=random_string_generator(size=4)
			)
		## repeatly check the uniqueness of new slug, return slug
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug
