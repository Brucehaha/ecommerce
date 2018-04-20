from django.db import models
from carts.models import Cart
from billing.models import BillingProfile
from addresses.models import Address
from ecommerce.utils import unique_order_id
from django.db.models.signals import pre_save, post_save
from decimal import *


ORDER_STATUS_CHOICES=(
	('created', 'Created'),
	('paid', 'Paid'),
	('shipped', 'Shipped'),
	('refund', 'refund'),


	)


class OrderManager(models.Manager):
	def new_or_get(self, billing_profile, cart_obj):
		'forbiden create new order with same cart repeately'
		qs = self.get_queryset().filter(cart=cart_obj, billing_profile=billing_profile, active=True)
		if qs.count()==1:
			obj = qs.first()
			new_obj = False
		else:
			# get rid of the olde order and create the new order --->the following code has been moved to the order manager
			# older_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
			# if older_order_qs.exists(): 
			# 	older_order_qs.update(active=False)
			obj = self.model.objects.create(
						billing_profile=billing_profile, 
						cart=cart_obj)
			new_obj = True
		return obj, new_obj
				



class Order(models.Model):
	billing_profile 	= models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.DO_NOTHING)
	shipping_address	= models.ForeignKey(Address, related_name='shipping', null=True, blank=True, on_delete=models.DO_NOTHING)
	billing_address		= models.ForeignKey(Address, related_name='billing', null=True, blank=True, on_delete=models.DO_NOTHING)
	order_id			= models.CharField(max_length=120, blank=True)
	cart  				= models.ForeignKey(Cart, on_delete=models.CASCADE)
	status				= models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	ship_total			= models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
	total				= models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
	active				= models.BooleanField(default=True)

	objects=OrderManager()

	def __str__(self) :
		return str(self.id)

	def update_total(self):
		cart_total = self.cart.total
		ship_total = self.ship_total
		self.total = round(Decimal(cart_total)+Decimal(ship_total),2)
		self.save() 


def pre_save_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id(instance)
	qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)


pre_save.connect(pre_save_order_id, sender=Order)




def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		cart_id = instance.id
		qs = Order.objects.filter(cart=cart_id)
		if qs.count() == 1:
			order_obj = qs.first()
			order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order_total(sender, instance, created, *args, **kwargs):
	if created:
		instance.update_total()

post_save.connect(post_save_order_total, sender=Order)