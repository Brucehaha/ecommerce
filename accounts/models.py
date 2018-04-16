from django.db import models



class GuestEmail(models.Model):
	email 		= models.EmailField()
	active  	= models.BooleanField(default=True)
	updated 	= models.DateTimeField()
	created 	= models.DateTimeField(editable=False)

	def __str__(self):
		return self.email