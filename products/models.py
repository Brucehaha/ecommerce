import random
import os
from datetime import date
from django.db import models

# Create your models here.
def get_filename_ext(filename):
	base_name = os.path.basename(filename)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	print(instance)
	print(filename)
	file_rand = random.randint(1, 1000000000)
	name, ext = get_filename_ext(filename)
	foldername = date.today().strftime('%Y%b%d')
	full_filename = 'products/{foldername}/{name}_{file_rand}.{ext}'.format(
		foldername=foldername, 
		name=name, 
		file_rand=file_rand, 
		ext=ext
		)

	return full_filename

class Product(models.Model):
	title 		= models.CharField(max_length=120)
	description = models.TextField()
	price		= models.DecimalField(decimal_places=2, max_digits=20, default=59)
	image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

	def __str__(self):
		return self.title
		
	def __unicode__(self):
		return self.title