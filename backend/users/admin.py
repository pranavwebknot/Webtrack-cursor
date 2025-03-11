from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'position', 'is_active', 'is_staff', 'is_verified')
    list_filter = ('role', 'department', 'is_active', 'is_staff', 'is_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'department', 'position')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'date_of_joining', 'profile_picture')}),
        (_('Professional info'), {'fields': ('role', 'department', 'position')}),
        (_('Status'), {'fields': ('is_active', 'is_staff', 'is_verified')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'department', 'position'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('date_joined', 'last_login')
        return ()
