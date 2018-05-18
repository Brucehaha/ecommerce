from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.utils import timezone
from accounts.models import GuestEmail
import stripe


STRIPE_PUBLIC_KEY = getattr(settings, 'STRIPE_PUBLIC_KEY', 'pk_test_G1nt8Wx2P97tG09vDwpkLQjs')
STRIPE_PRIVATE_KEY = getattr(settings, 'STRIPE_PRIVATE_KEY', 'sk_test_KRibT0JWeBwggF5iksBZ6y3j')
stripe.api_key=STRIPE_PRIVATE_KEY


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
	customer_id = models.CharField(max_length=120, blank=True, null=True)
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

def pre_save_user(sender, instance, *args, **kwargs):
	if not instance.customer_id and instance.email:
		customer = stripe.Customer.create(
			email = instance.email
		)
		instance.customer_id=customer.id

pre_save.connect(pre_save_user, sender=BillingProfile)


def post_save_user(sender, instance, created, *args, **kwargs):
	if not created:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(post_save_user, sender=User)
