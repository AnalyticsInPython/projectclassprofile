from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from access_control.models import AuthorizedEmail


@override_settings(CLASS_ACCESS_CODE="example-class-code")
class LoginTests(TestCase):
    def setUp(self):
        cache.clear()
        AuthorizedEmail.objects.create(normalized_email="student@example.edu")

    def test_valid_credentials_create_access_session(self):
        response = self.client.post(
            reverse("access_control:login"),
            {
                "email": " Student@Example.edu ",
                "access_code": "example-class-code",
            },
        )

        self.assertRedirects(response, reverse("profiles:list"))
        self.assertTrue(self.client.session[settings.ACCESS_SESSION_KEY])

    def test_invalid_credentials_return_generic_error(self):
        response = self.client.post(
            reverse("access_control:login"),
            {"email": "student@example.edu", "access_code": "wrong"},
        )

        self.assertContains(response, "Email address or access code is incorrect.")
        self.assertNotIn(settings.ACCESS_SESSION_KEY, self.client.session)

    def test_logout_clears_access_session(self):
        session = self.client.session
        session[settings.ACCESS_SESSION_KEY] = True
        session.save()

        response = self.client.post(reverse("access_control:logout"))

        self.assertRedirects(response, reverse("access_control:login"))
        self.assertNotIn(settings.ACCESS_SESSION_KEY, self.client.session)

    def test_repeated_failures_are_rate_limited(self):
        for _ in range(settings.LOGIN_FAILURE_LIMIT + 1):
            response = self.client.post(
                reverse("access_control:login"),
                {"email": "student@example.edu", "access_code": "wrong"},
            )

        self.assertContains(response, "Email address or access code is incorrect.")
        self.assertNotIn(settings.ACCESS_SESSION_KEY, self.client.session)
