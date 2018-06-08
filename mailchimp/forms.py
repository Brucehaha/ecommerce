from django.forms import ModelForm
from .models import Mailchimp


class MailchimpForm(ModelForm):
    class Meta:
        model = Mailchimp
        fields = ['subscribed']
