from django.urls import path

from . import views


app_name = "profiles"

urlpatterns = [
    path("", views.profile_list, name="list"),
    path("profile-photo/<int:profile_id>/", views.profile_photo, name="photo"),
]

