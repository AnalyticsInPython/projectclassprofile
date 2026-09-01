from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_linkedin_url(value):
    if not value:
        return
    hostname = (urlparse(value).hostname or "").lower()
    if hostname not in {"linkedin.com", "www.linkedin.com"}:
        raise ValidationError("Enter a valid LinkedIn profile URL.")

