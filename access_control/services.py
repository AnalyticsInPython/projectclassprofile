import secrets

from django.conf import settings
from django.core.cache import cache

from .models import AuthorizedEmail


def normalize_email(email):
    return email.strip().lower()


def _client_key(request):
    address = request.META.get("REMOTE_ADDR", "unknown")
    return f"class-profile-login:{address}"


def is_rate_limited(request):
    attempts = cache.get(_client_key(request), 0)
    return attempts >= settings.LOGIN_FAILURE_LIMIT


def record_failed_attempt(request):
    key = _client_key(request)
    attempts = cache.get(key, 0) + 1
    cache.set(key, attempts, timeout=settings.LOGIN_BLOCK_SECONDS)


def clear_failed_attempts(request):
    cache.delete(_client_key(request))


def credentials_are_valid(email, access_code):
    normalized_email = normalize_email(email)
    email_allowed = AuthorizedEmail.objects.filter(
        normalized_email=normalized_email,
        is_active=True,
    ).exists()

    configured_code = settings.CLASS_ACCESS_CODE
    code_allowed = bool(configured_code) and secrets.compare_digest(
        access_code,
        configured_code,
    )
    return email_allowed and code_allowed


def grant_access(request, email):
    request.session.cycle_key()
    request.session[settings.ACCESS_SESSION_KEY] = True
    request.session["access_email"] = normalize_email(email)


def revoke_access(request):
    request.session.flush()

