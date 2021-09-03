from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    exclude = ()


admin.site.register(UserProfile, UserProfileAdmin)
