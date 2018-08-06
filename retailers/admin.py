from django.contrib import admin
from .models import Sample, Retailer, SampleBridge
from django.contrib import admin


class SampleBridgeInline(admin.TabularInline):
    model = SampleBridge

class RetailerAdmin(admin.ModelAdmin):
    inlines =(SampleBridgeInline,)
    list_display = ('business_name','first_name', 'last_name','phone_number','is_active')

class SampleAdmin(admin.ModelAdmin):
    inlines =(SampleBridgeInline,)
    list_display = ('title','price', 'image','active')



admin.site.register(Sample, SampleAdmin)
admin.site.register(Retailer, RetailerAdmin)
