from django.db import models
from django.conf import settings
from .utils import MailchimpHandler
from django.db.models.signals import pre_save, post_save


User = settings.AUTH_USER_MODEL


class Mailchimp(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed      = models.BooleanField(default=True)
    messages        = models.TextField(null=True, blank=True)
    timestamps      = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

def post_save_mailchimp(sender, instance, created, *args, **kwargs):
	if created:
		MailchimpHandler().add(instance.user.email)

post_save.connect(post_save_mailchimp, sender=User)

def pre_save_mailchimp(sender, instance, *args, **kwargs):
    #check user status in Mailchimp
    #if changed, update instance
    response_code, response_dict = MailchimpHandler().status_check(instance.)
    instance.messages =

pre_save.connect(post_save_mailchimp, sender=Mailchimp)
