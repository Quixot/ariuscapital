from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'last_login')
    list_display_links = ('id', 'username', 'email')

admin.site.register(User, UserAdmin)
