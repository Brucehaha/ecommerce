from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
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
			request.session['cart_items'] = cart_obj.products.count()
			if  cart_obj.user is None:
				if request.user.is_authenticated:
					cart_obj.user = request.user
					cart_obj.save()
		else:
			cart_obj = Cart.objects.new(user=request.user)
			new_object = True
			request.session['cart_id'] = cart_obj.id

		return cart_obj, new_object

	def load_cart(self, request):
		user = request.user
		## loading cart when login, if there is cart session
		cart_id = request.session.get("cart_id") or None
		if user.is_authenticated and cart_id is None:
			if user.cart_set.all().filter(active=True).exists():
				cart_objs = user.cart_set.all().filter(active=True)
				cart_obj = cart_objs.last()
				request.session['cart_items'] = cart_obj.products.count()
				request.session["cart_id"] = cart_obj.id

	def new(self, user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated :
				user_obj = user
		return self.model.objects.create(user=user_obj)




class Cart(models.Model):
	user		= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	products	= models.ManyToManyField(Product, through='Entry', blank=True)
	subtotal	= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	total		= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	updated		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	active		= models.BooleanField(default=True)

	objects=CartManager()

	def __str__(self):
		return str(self.id)

	def cart_checkout(self):
		self.active = False
		self.save()


class Entry(models.Model):
    cart		= models.ForeignKey(Cart, on_delete=models.CASCADE)
    product		= models.ForeignKey(Product, on_delete=models.CASCADE)
    area		= models.DecimalField(default=100, max_digits=11, decimal_places=2)
    packs       = models.IntegerField(default=100)
    total		= models.DecimalField(default=0.00, max_digits=11, decimal_places=2)
    updated		= models.DateTimeField(auto_now=True)
    timestamp	= models.DateTimeField(auto_now_add=True)


def entry_pre_save(sender, instance, *args, **kwargs):
    price = instance.product.price
    size = instance.product.size
    packs = instance.packs
    area = round(size*Decimal(packs),2)
    total = round(area*price,2)
    instance.area = area
    instance.total = total

pre_save.connect(entry_pre_save, sender=Entry)

def entry_post_save(sender, instance, created, *args, **kwargs):
    if created:
        cart_obj = instance.cart
        subtotal = 0
        for entry in cart_obj.entry_set.all():
            subtotal += entry.total
        cart_obj.subtotal = subtotal
        cart_obj.total = round(subtotal*Decimal(1.1),2)
        cart_obj.save()

post_save.connect(entry_post_save, sender=Entry)

def entry_post_delete(sender, instance, *args, **kwargs):
    cart_obj = instance.cart
    subtotal = 0
    for entry in cart_obj.entry_set.all():
        subtotal += entry.total
    cart_obj.subtotal = subtotal
    cart_obj.total = round(subtotal*Decimal(1.1),2)
    cart_obj.save()

post_delete.connect(entry_post_delete, sender=Entry)
