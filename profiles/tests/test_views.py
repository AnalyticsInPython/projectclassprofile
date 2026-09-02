from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from profiles.models import Profile


class ProfileViewTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            full_name="Example Student",
            cbs_email="student@example.edu",
            consent_confirmed_at=timezone.now(),
        )

    @override_settings(REQUIRE_CLASS_LOGIN=True)
    def test_directory_redirects_without_access_session_when_login_is_required(self):
        response = self.client.get(reverse("profiles:list"))
        self.assertRedirects(response, "/login/?next=%2F")

    @override_settings(REQUIRE_CLASS_LOGIN=False)
    def test_directory_is_public_when_login_is_disabled(self):
        response = self.client.get(reverse("profiles:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example Student")

    def test_directory_hides_email_address(self):
        session = self.client.session
        session[settings.ACCESS_SESSION_KEY] = True
        session.save()

        response = self.client.get(reverse("profiles:list"))

        self.assertContains(response, "Example Student")
        self.assertNotContains(response, "student@example.edu")

    def test_missing_photo_returns_private_placeholder(self):
        session = self.client.session
        session[settings.ACCESS_SESSION_KEY] = True
        session.save()

        response = self.client.get(reverse("profiles:photo", args=[self.profile.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/svg+xml")
        self.assertEqual(response["Cache-Control"], "private, no-store")
