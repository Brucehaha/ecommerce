from django.contrib import admin
from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import GuestEmail
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()

class MyUserAdmin(UserAdmin):
    search_fields = ['email']
    form =UserAdminChangeForm
    add_form = UserAdminCreationForm
     # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin','staff', 'active',)
    fieldsets = (
        (None, {'fields':('email', 'password',)}),
        ('Personal info',{'fields':('username', 'first_name','last_name',)}),
        ('Permissions', {'fields':('admin','staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering =('email', )
    filter_horizontal = ()

admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail
admin.site.register(GuestEmail)
