from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from decimal import *

from products.models import Product

User = settings.AUTH_USER_MODEL 

class CartManager(models.Manager):
	def new_or_get(self, request):
		user = request.user
		cart_id = None
	
		cart_id =request.session.get("cart_id", None)
		qs = self.get_queryset().filter(id=cart_id, active=True)
		if qs.count() == 1:
			new_object = False
			cart_obj = qs.first()
			if  cart_obj.user is None:
				if request.user.is_authenticated:
					cart_obj.user = request.user
					cart_obj.save()
		else:
			cart_obj = Cart.objects.new(user=request.user)
			new_object = True
			request.session['cart_id'] = cart_obj.id

		request.session['cart_items'] = cart_obj.products.count()
		return cart_obj, new_object
	def load_cart(self, request):
		user = request.user
		cart_id = request.session.get("cart_id") or None
		if user.is_authenticated and not cart_id:
			cart_objs = user.cart_set.all() or None
			if cart_objs:
				for i in cart_objs:
					if i.active == True:
						cart_obj = i
						cart_id = cart_obj.id
						request.session['cart_items'] = cart_obj.products.count()
						request.session["cart_id"] = cart_id
						break
			


	def new(self, user=None):
		user_obj = None 
		if user is not None:
			if user.is_authenticated :
				user_obj = user
		return self.model.objects.create(user=user_obj)



class Cart(models.Model):
	user		= models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
	products	= models.ManyToManyField(Product, blank=True)
	subtotal	= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	total		= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	updated		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	active		= models.BooleanField(default=True)

	objects=CartManager()

	def __str__(self):
		return str(self.id)


def cart_m2m_changed(sender, instance, action, *args, **kwargs):
	if action in ["post_clear", "post_remove", "post_add"]:
		products = instance.products.all()
		total = 0
		for x in products: 
			total += x.price
		instance.subtotal = total
		instance.save()

m2m_changed.connect(cart_m2m_changed, sender=Cart.products.through)




def cart_pre_save(sender, instance, *args, **kwargs):
	instance.total = Decimal(instance.subtotal)*Decimal(1.1)

pre_save.connect(cart_pre_save, sender=Cart)

