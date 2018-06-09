from django.db import models
from django.conf import settings
from .utils import MailchimpHandler
from django.db.models.signals import pre_save, post_save


User = settings.AUTH_USER_MODEL


class Mailchimp(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed              = models.BooleanField(default=True)
    mailchimp_subscribed    = models.NullBooleanField(blank=True)
    messages                = models.TextField(null=True, blank=True)
    timestamps              = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

def post_save_mailchimp(sender, instance, created, *args, **kwargs):
    if created:
        response_code, response_dict = MailchimpHandler().add(instance.user.email)

post_save.connect(post_save_mailchimp, sender=Mailchimp)


def pre_save_mailchimp(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed == True:
            response_code, response_dict = MailchimpHandler().subscribe(instance.user.email)
        else:
            response_code, response_dict = MailchimpHandler().unsubscribe(instance.user.email)

        if response_dict.get("status") == "subscribed":
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.messages = response_dict
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.messages = response_dict

pre_save.connect(pre_save_mailchimp, sender=Mailchimp)
