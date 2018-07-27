from django.forms.models import BaseModelFormSet

class CartFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(CartFormSet, self).__init__(*args, **kwargs)
        for product in self.instance.product.all():
            #skip extra forms
            form.fields['product'].initial= form.product
