from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.utils import timezone
from accounts.models import GuestEmail



User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		guest_email_id = request.session.get('guest_email_id')
		user = request.user 
		obj = None
		created = False

		if user.is_authenticated:
			'logged in user checkout'
			obj, created= self.model.objects.get_or_create(user=user, email=user.email)
			'guest user checkout'
		elif guest_email_id is not None:
			guest_email_obj, new_guest_email_obj= GuestEmail.objects.get_or_create(email=guest_email_id)
			obj, created  = self.model.objects.get_or_create(email=guest_email_obj)
		return obj, created


class BillingProfile(models.Model):
	user 		= models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
	email		= models.EmailField()
	active  	= models.BooleanField(default=True)
	updated 	= models.DateTimeField()
	created 	= models.DateTimeField(editable=False)


	objects=BillingProfileManager()

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