from django.contrib import admin
from .models import User


# Register your models here.

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'is_superuser', 'is_staff', 'username', 'first_name', 'last_name', 'groups', 'user_permissions', 'email',
        'is_verified',
        'is_active')

    class Meta:
        model = User
