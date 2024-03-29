from django.contrib import admin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('age',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',
                                    'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )