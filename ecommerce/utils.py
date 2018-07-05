import random
import string
##slugify separete word with dash
from django.utils.text import slugify


def random_string_generator(size=10, chars=(string.ascii_lowercase + string.digits)):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_key_id(instance):
	size = random.randint(30, 45)
	key = random_string_generator(size=size)
	klass = instance.__class__
	qs = klass.objects.filter(key=key)
	if qs:
		return unique_order_id(instance)
	return key

def unique_order_id(instance):
	order_id = random_string_generator(10).upper()
	klass = instance.__class__
	qs = klass.objects.filter(order_id=order_id)
	if qs:
		return unique_order_id(instance)
	return order_id


def unique_slug_generator(instance, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title)

	klass = instance.__class__
	qs = klass.objects.filter(slug=slug)
	if qs:
		new_slug = "{slug}-{randstr}".format(
				slug=slug,
				randstr=random_string_generator(size=4)
			)
		## repeatly check the uniqueness of new slug, return slug
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug
