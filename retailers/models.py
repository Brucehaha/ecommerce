from django.db import models
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.validators import RegexValidator
import random
import os
from datetime import date


User = settings.AUTH_USER_MODEL

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    file_rand = random.randint(1, 1000000000)
    name, ext = get_filename_ext(filename)
    foldername = date.today().strftime('%Y%b%d')
    full_filename = 'samples/{foldername}/{name}_{file_rand}.{ext}'.format(
        foldername=foldername,
        name=name,
        file_rand=file_rand,
        ext=ext
        )
    return full_filename

class Sample(models.Model):
    title           = models.CharField(max_length=120)
    slug            =models.SlugField(blank=True, unique=True)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2,max_digits=11, default=0)
    image           = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def sample_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(sample_pre_save_receiver, sender=Sample)


class Retailer(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    email           = models.EmailField(verbose_name='email address',max_length=255)
    sample          = models.ManyToManyField(Sample, through='SampleBridge', blank=True)
    business_name   = models.CharField(max_length=255, blank=True, null=True)
    latitude        = models.DecimalField(decimal_places=15,max_digits=20, default=0)
    longitude       = models.DecimalField(decimal_places=15,max_digits=20, default=0)
    first_name      = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name       = models.CharField(verbose_name='last name', max_length=30, blank=True)
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number    = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return str(self.business_name)


class SampleBridge(models.Model):
    sample		= models.ForeignKey(Sample, on_delete=models.CASCADE)
    retailer    = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    number      = models.IntegerField(default=1)
    updated		= models.DateTimeField(auto_now=True)
    timestamp	= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sample
