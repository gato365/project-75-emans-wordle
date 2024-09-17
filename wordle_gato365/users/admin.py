from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


## Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

## Define a new UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'college', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'graduating_class', 'college', 'major')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'graduating_class', 'college', 'major')}),
    )

## Register the new UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)