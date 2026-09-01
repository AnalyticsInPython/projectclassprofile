from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import AccessForm
from .services import (
    clear_failed_attempts,
    credentials_are_valid,
    grant_access,
    is_rate_limited,
    record_failed_attempt,
    revoke_access,
)


GENERIC_LOGIN_ERROR = "Email address or access code is incorrect."


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.session.get(settings.ACCESS_SESSION_KEY):
        return redirect("profiles:list")

    next_url = request.GET.get("next") or request.POST.get("next") or reverse(
        "profiles:list"
    )
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = reverse("profiles:list")

    form = AccessForm(request.POST or None)
    error = ""

    if request.method == "POST" and form.is_valid():
        if is_rate_limited(request):
            error = GENERIC_LOGIN_ERROR
        elif credentials_are_valid(
            form.cleaned_data["email"],
            form.cleaned_data["access_code"],
        ):
            clear_failed_attempts(request)
            grant_access(request, form.cleaned_data["email"])
            return redirect(next_url)
        else:
            record_failed_attempt(request)
            error = GENERIC_LOGIN_ERROR

    return render(
        request,
        "access_control/login.html",
        {"form": form, "error": error, "next": next_url},
    )


@require_POST
def logout_view(request):
    revoke_access(request)
    return redirect("access_control:login")

