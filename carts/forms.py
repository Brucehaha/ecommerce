from .models import Entry, Cart
from django.forms import ModelForm
from django.forms import modelformset_factory,inlineformset_factory

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['packs']


EntryFormSet = modelformset_factory(Entry, form=EntryForm)

inlineFormSet = inlineformset_factory(Cart, Entry, form=EntryForm, extra=0 ,can_delete=True)
