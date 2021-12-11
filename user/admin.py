from django.contrib import admin
from .models import User


# Register your models here.

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'is_superuser', 'is_staff', 'is_verified', 'is_active',
        'username', 'first_name', 'last_name', 'email', 'phone_number',
        'groups', 'user_permissions'
    )

    class Meta:
        model = User
