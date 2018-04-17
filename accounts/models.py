from django.db import models
from django.utils import timezone


class GuestEmail(models.Model):
	email 		= models.EmailField()
	active  	= models.BooleanField(default=True)
	updated 	= models.DateTimeField()
	created 	= models.DateTimeField(editable=False)

	def __str__(self):
		return self.email
	
	def save(self, *args, **kwargs):
		''' On save, update timestamps'''
		if not self.id:
			self.created=timezone.now()
		self.updated = timezone.now()
		return super(GuestEmail, self).save(*args, **kwargs)