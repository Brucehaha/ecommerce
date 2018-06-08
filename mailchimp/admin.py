from django.contrib import admin
from .models import Mailchimp

class MilcimpAdmin(admin.ModelAdmin):
    readonly_fields = ('mailchimp_subscribed',
                       'updated', 'timestamps',
                       'messages')
    list_display =('__str__', 'subscribed', 'updated')

admin.site.register(Mailchimp, MilcimpAdmin)
