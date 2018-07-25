from django.db import models
from django.urls import reverse
from carts.models import Cart
from billing.models import BillingProfile
from addresses.models import Address
from ecommerce.utils import unique_order_id
from django.db.models.signals import pre_save, post_save
from decimal import *

import math
import datetime
from django.conf import settings
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from carts.models import Cart
from products.models import Product


ORDER_STATUS_CHOICES=(
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refund', 'refund'),


    )

class OrderManagerQuerySet(models.query.QuerySet):
    def not_created(self):
        return self.exclude(status='created')
    def by_status(self, status='shipped'):
        return self.recent().filter(status=status)
    def recent(self):
        return self.order_by('-updated','-timestamp')

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def new_or_get(self, billing_profile, cart_obj):
        qs = self.get_queryset().filter(cart=cart_obj,
                                        billing_profile=billing_profile,
                                        active=True,
                                        status='created')
        if qs.count()==1:
            obj = qs.first()
            new_obj = False
        else:
            # get rid of the olde order and create the new order --->the following code has been moved to the order manager
            # older_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            # if older_order_qs.exists():
            #     older_order_qs.update(active=False)
            obj = self.model.objects.create(
                        billing_profile=billing_profile,
                        cart=cart_obj)
            new_obj = True
        return obj, new_obj
    def list_order(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile=billing_profile)
        return qs


class Order(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL)
    shipping_address        = models.ForeignKey(Address, related_name='shipping', null=True, blank=True, on_delete=models.DO_NOTHING)
    billing_address         = models.ForeignKey(Address, related_name='billing', null=True, blank=True, on_delete=models.DO_NOTHING)
    order_id                = models.CharField(max_length=120, blank=True)
    cart                    = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status                  = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    ship_total              = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    total                   = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    active                  = models.BooleanField(default=True)
    updated                 = models.DateTimeField(auto_now=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects=OrderManager()
    class Meta:
        ordering = ["-updated", "-timestamp"]

    def __str__(self) :
        return str(self.id)

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("orders:detail", kwargs={"id": self.order_id})

    def update_total(self):
        cart_total = self.cart.total
        ship_total = self.ship_total
        self.total = round(Decimal(cart_total)+Decimal(ship_total),2)
        self.save()

    def check_done(self):
        shipping_address = self.shipping_address
        billing_address = self.billing_profile
        total = self.total
        billing_profile = self.billing_profile
        if shipping_address and billing_profile and billing_profile and total > 0:
            return True
        return False
    def mark_paid(self):
        if self.check_done:
            self.status = "paid"
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
