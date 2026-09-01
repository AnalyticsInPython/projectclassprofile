from django.test import TestCase
from django.utils import timezone

from profiles.models import Profile


class ProfileModelTests(TestCase):
    def test_email_is_normalized_on_save(self):
        profile = Profile.objects.create(
            full_name="Example Student",
            cbs_email="  Student@Example.edu ",
            consent_confirmed_at=timezone.now(),
        )
        self.assertEqual(profile.cbs_email, "student@example.edu")

