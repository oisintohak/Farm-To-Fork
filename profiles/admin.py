from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    exclude = ()
    readonly_fields = ['user']


admin.site.register(UserProfile, UserProfileAdmin)
