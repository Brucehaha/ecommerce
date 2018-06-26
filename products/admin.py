from django.contrib import admin
#ll
from .models import Product


class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class meta:
			model=Product

admin.site.register(Product, ProductAdmin)
