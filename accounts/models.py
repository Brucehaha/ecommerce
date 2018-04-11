from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.utils import timezone



User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
	user 		= models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
	email		= models.EmailField()
	updated 	= models.DateTimeField()
	created 	= models.DateTimeField(editable=False)

	def save(self, *args, **kwargs):
		''' On save, update timestamps'''
		if not self.id:
			self.created=timezone.now()
		self.updated = timezone.now()
		return super(BillingProfile, self).save(*args, **kwargs)

def post_save_user(sender, instance, created, *args, **kwargs):
	if not created:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(post_save_user, sender=User)