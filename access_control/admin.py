from django.contrib import admin

from .models import AuthorizedEmail


@admin.register(AuthorizedEmail)
class AuthorizedEmailAdmin(admin.ModelAdmin):
    list_display = ("normalized_email", "is_active")
    list_filter = ("is_active",)
    search_fields = ("normalized_email",)

