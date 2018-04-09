from django.db import models
from carts.models import Cart
from ecommerce.utils import unique_order_id
from math import fsum
from django.db.models.signals import pre_save, post_save

ORDER_STATUS_CHOICES=(
	('created', 'Created'),
	('paid', 'Paid'),
	('shipped', 'Shipped'),
	('refund', 'refund'),


	)


class Order(models.Model):
	order_id	= models.CharField(max_length=120, blank=True)
	cart  		= models.ForeignKey(Cart, on_delete=models.CASCADE)
	status		= models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	ship_total	= models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
	total		= models.DecimalField(default=5.99, max_digits=200, decimal_places=2)

	def __str__(self):
		return self.order_id

	def update_total(self):
		cart_total = self.cart.total
		ship_total = self.ship_total
		self.total = fsum([cart_total, ship_total])
		self.save()


def pre_save_order_id(sender, instance, *args, **kwargs):
	instance.order_id = unique_order_id(instance)

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