from django.contrib import admin
from .models import Organization, Role, User
# Register your models here.
# admin.site.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')  # Show 'role' in the user list
    list_filter = ('role',)  # Filter by role
    search_fields = ('username', 'email')  # Enable searching by username or email
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    # To include role in the 'add user' form
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)