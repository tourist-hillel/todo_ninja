from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users_app.models import ToDoUser


class CustomUserAdmin(UserAdmin):
    model = ToDoUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ('User creation', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'date_of_birth'),
        }),
    )

    ordering = ['email']
    list_filter = ('is_active', 'is_staff', 'date_joined')
    


admin.site.register(ToDoUser, CustomUserAdmin)
