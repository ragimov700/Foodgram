from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email',)
    list_display = ('username', 'email', 'first_name', 'last_name',)
    search_fields = ('username', 'email',)


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
