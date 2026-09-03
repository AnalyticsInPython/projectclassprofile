import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from access_control.decorators import class_access_required

from .models import Profile
from .search import search_profiles


@require_GET
@class_access_required
def profile_list(request):
    query = request.GET.get("q", "").strip()
    profiles = search_profiles(Profile.objects.all(), query)
    return render(
        request,
        "profiles/profile_list.html",
        {"profiles": profiles, "query": query},
    )


@require_GET
@class_access_required
def profile_photo(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if profile.photo:
        try:
            profile.photo.open("rb")
        except (FileNotFoundError, OSError):
            pass
        else:
            content_type, _ = mimetypes.guess_type(profile.photo.name)
            response = FileResponse(
                profile.photo.file,
                content_type=content_type or "application/octet-stream",
            )
            response["Cache-Control"] = "private, no-store"
            response["X-Content-Type-Options"] = "nosniff"
            return response

    placeholder = settings.BASE_DIR / "static" / "images" / "profile-placeholder.svg"
    if not Path(placeholder).is_file():
        raise Http404("Profile photograph is unavailable.")
    response = FileResponse(placeholder.open("rb"), content_type="image/svg+xml")
    response["Cache-Control"] = "private, no-store"
    return response

