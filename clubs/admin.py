"""Configuration of the admin interface for clubs."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Club, ClubContract
from django.utils.translation import ugettext_lazy as _


class ChessUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, ChessUserAdmin)
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'club_name', 'club_location', 'club_description',
    ]

@admin.register(ClubContract)
class ContractAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for contracts."""

    list_display = [
        'user', 'club', 'role',
    ]
