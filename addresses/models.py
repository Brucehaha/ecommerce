from django.db import models
from billing.models import BillingProfile
from django.urls import reverse

ADDRESS_TYPE = (
	('shipping', 'Shipping'),
	('billing', 'Billing')
	)


class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
	address_type	= models.CharField(max_length=120, choices=ADDRESS_TYPE)
	address_line1	= models.CharField(max_length=120)
	address_line2	= models.CharField(max_length=120, null=True, blank=True)
	suburb			= models.CharField(max_length=120)
	state			= models.CharField(max_length=120)
	country			= models.CharField(max_length=120, default='Australia')
	postcode	    = models.CharField(max_length=120)


	def __str__(self):
		return str(self.billing_profile)

	def get_absolute_url(self):
		return reverse("address-update", kwargs={"pk": self.pk})

	def get_address(self):
		return '{address_line1} {address_line2} {suburb} {state} {country} {postcode}'.format(
				address_line1 = self.address_line1,
				address_line2 = self.address_line2,
				suburb		  = self.suburb,
				state		  = self.state,
				country       = self.country,
				postcode	  = self.postcode

			)
