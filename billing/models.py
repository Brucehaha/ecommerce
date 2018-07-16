from django.db import models
from django.urls import reverse
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
			guest_email_obj = GuestEmail.objects.get(email=guest_email_id)
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

	def __str__(self):
		return str(self.email)

	def save(self, *args, **kwargs):
		''' On save, update timestamps'''
		if not self.id:
			self.created=timezone.now()
		self.updated = timezone.now()
		return super(BillingProfile, self).save(*args, **kwargs)

	def charge(self, order_obj, card=None):
		return Charge.objects.do(self, order_obj, card)

	def get_cards(self):
		return self.card_set.all()

	def deactivate_card(self):
		cards = self.get_cards()
		cards.update(active=False)
		return cards.filter(active=True).count()

	def get_payment_method_url(self):\
		return reverse('payment_method')

	@property
	def has_card(self):
		card_qs = self.get_cards()
		return card_qs.exists()
	@property
	def default_cards(self):
		default_cards= self.get_cards().filter(default=True, active=True)
		if default_cards.exists():
			return default_cards.last()
		return None

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


class CardManager(models.Manager):
	def new_or_get(self, billing_profile, card_info, token):
		if str(card_info.object=='card'):
			obj= self.model(
				billing=billing_profile,
				card_id=card_info.id,
				name=card_info.name,
				brand=card_info.brand,
				country=card_info.country,
				last4=card_info.last4,
				cvc_check=card_info.cvc_check,
				exp_month=card_info.exp_month,
				exp_year=card_info.exp_year,
				source=token
				)
			obj.save()
		return obj

	def all(self):
		return self.get_queryset().filter(active=True)


class Card(models.Model):
	billing 		= models.ForeignKey(BillingProfile,on_delete=models.CASCADE, null=True, blank=True)
	card_id			= models.CharField(max_length=120, blank=True, null=True)
	name			= models.CharField(max_length=120, blank=True, null=True)
	brand 			= models.CharField(max_length=120, blank=True, null=True)
	country 		= models.CharField(max_length=50, blank=True, null=True)
	last4			= models.CharField(max_length=20, blank=True, null=True)
	cvc_check		= models.CharField(max_length=20, blank=True, null=True)
	exp_month		= models.IntegerField(blank=True, null=True)
	exp_year 		= models.IntegerField(blank=True, null=True)
	source			= models.CharField(max_length=120, blank=True, null=True)
	default			= models.BooleanField(default=True)
	active			= models.BooleanField(default=True)
	timestamps 		= models.DateTimeField(auto_now_add=True)

	objects = CardManager()

	def __str__(self):
		return "{} {}".format(self.brand,self.last4)


def post_save_card(sender, instance, created, *args, **kwargs):
	if created:
		qs = Card.objects.filter(billing=instance.billing).exclude(id=instance.id)
		qs.update(default=False)

post_save.connect(post_save_card, sender=Card)



class ChargeManager(models.Manager):
	def do(self, billing, order_obj, card=None):
		card_obj = card
		if card_obj is None:
			cards= billing.card_set.filter(default=True)
			if cards.exists():
				card=cards.first()

		c = stripe.Charge.create(
			  amount=int(order_obj.total*100),
			  currency="aud",
			  customer=billing.customer_id,
			  source=card.card_id, # obtained with Stripe.js
			  description="Charge for {}".format(billing.email),
			  metadata={"order_id": order_obj.order_id}
			)
		new_charge = self.model(
				billing 		= billing,
				charge_id		= c.id,
				amount			= c.amount,
				amount_refunded = c.amount_refunded,
				customer_id		= c.customer,
				paid 			= c.paid,
				refunded 		= c.refunded,
				created			= c.created,
				failure_message = c.failure_message,
				status 			= c.status,
				outcome			= c.outcome,
				description		= c.description
		)
		new_charge.save()
		return new_charge

class Charge(models.Model):
	billing 		= models.ForeignKey(BillingProfile,on_delete=models.CASCADE, null=True, blank=True)
	charge_id		= models.CharField(max_length=120, blank=True, null=True)
	amount			= models.IntegerField(blank=True, null=True)
	amount_refunded = models.IntegerField(blank=True, null=True)
	customer_id		= models.CharField(max_length=120, blank=True, null=True)
	paid 			= models.CharField(max_length=120, blank=True, null=True)
	refunded 		= models.CharField(max_length=50, blank=True, null=True)
	created			= models.CharField(max_length=20, blank=True, null=True)
	outcome			= models.TextField(blank=True, null=True)
	failure_message = models.TextField(blank=True, null=True)
	status 			= models.CharField(max_length=50, blank=True, null=True)
	description		= models.CharField(max_length=120, blank=True, null=True)

	objects = ChargeManager()
