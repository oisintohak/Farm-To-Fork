from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserModel


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserModel
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'first_name',
                   'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username',
         'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':
                (
                    'email',
                    'username',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_active',
            )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(UserModel, CustomUserAdmin)
