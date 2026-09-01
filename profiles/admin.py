from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "cbs_email",
        "country_of_origin",
        "desired_industry",
        "consent_confirmed_at",
    )
    search_fields = (
        "full_name",
        "cbs_email",
        "previous_employment",
        "desired_industry",
    )

