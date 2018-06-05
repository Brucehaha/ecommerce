from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL
class Mailchimp(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed      = models.BooleanField(default=True)
    messages        = models.TextField(null=True, blank=True)
    timestamps      =models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
