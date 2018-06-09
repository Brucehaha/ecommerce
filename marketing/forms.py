from django import forms
from .models import Mailchimp


class MailchimpForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)
    class Meta:
        model = Mailchimp
        fields = ['subscribed']
