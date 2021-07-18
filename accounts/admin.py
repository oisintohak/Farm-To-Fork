from typing import Set


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import UserModel


class CustomUserAdmin(UserAdmin):
    model = UserModel
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields':
                (
                    'email',
                    'first_name',
                    'last_name',
                    'user_type',
            )}
         ),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields':
                (
                    'user_type',
            )}
         ),
    )
    readonly_fields = [
        'date_joined',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(UserModel, CustomUserAdmin)
