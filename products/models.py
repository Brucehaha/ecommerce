import random
import os
from datetime import date
from django.db import models
from django.db.models.signals import pre_save, post_save
from.utils import unique_slug_generator


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


class ProductQuerySet(models.query.QuerySet):
	def featured(self): #for Product.objects.all().featured()
		return self.filter(featured=True, active=True)

	def active(self):
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def features(self):#for Product.objects.featured
		return self.get_queryset() .filter(featured=True)

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None

class Product(models.Model):
	title 		= models.CharField(max_length=120)
	slug		=models.SlugField(blank=True, unique=True)
	description = models.TextField()
	price		= models.DecimalField(decimal_places=2,
	 								  max_digits=20,
	 								  default=59
	 								 )
	image       = models.ImageField(upload_to=upload_image_path,
									null=True, 
									blank=True
									)
	featured	= models.BooleanField(default=False)
	active		= models.BooleanField(default=True)

	objects = ProductManager()

	def __str__(self):
		return self.title
		
	def __unicode__(self):
		return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)