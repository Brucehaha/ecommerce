from django.db import models
from billing import BillingProfile


ADDRESS_TYPE = (
	('shipping', 'Shipping'),
	('billing', 'Billing')
	)


class Address(models.Model):
	billing_profile = models.Foreignkey(BillingProfile)
	address_type	= models.CharField(max_length=120, choices=ADDRESS_TYPE)
	address_line1	= models.CharField(max_length=120)
	address_line2	= models.CharField(max_length=120, null=True, blank=True)
	suburb			= models.CharField(max_length=120)
	state			= models.CharField(max_length=120)
	country			= models.CharField(max_length=120, default='Australia')
	postcode	    = models.CharField(max_length=120)


	def __str__(self):
		return str(self.billing_profile)

