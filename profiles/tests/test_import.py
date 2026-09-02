import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase

from access_control.models import AuthorizedEmail
from profiles.models import Profile


class ImportProfilesTests(TestCase):
    def test_import_accepts_current_approved_export_columns(self):
        with TemporaryDirectory() as directory:
            csv_path = Path(directory) / "approved_profiles.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "full_name",
                        "csb_email",
                        "country_of_origin",
                        "previous_employment",
                        "desired_industry",
                        "hobbies",
                        "linkedin_url",
                        "photo_filename",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "full_name": "Current Export Student",
                        "csb_email": "Current.Student@Example.edu",
                        "country_of_origin": "Japan",
                        "previous_employment": "Example Health",
                        "desired_industry": "Healthcare",
                        "hobbies": "Running",
                        "linkedin_url": "https://www.linkedin.com/in/example-current",
                        "photo_filename": "",
                    }
                )

            call_command("import_profiles", csv_path)

        profile = Profile.objects.get(cbs_email="current.student@example.edu")
        self.assertEqual(profile.undergraduate_institution, "")
        self.assertIsNone(profile.age)
        self.assertTrue(
            AuthorizedEmail.objects.filter(
                normalized_email="current.student@example.edu",
                is_active=True,
            ).exists()
        )

    def test_import_creates_profile_and_allowlist_entry(self):
        with TemporaryDirectory() as directory:
            csv_path = Path(directory) / "profiles.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "full_name",
                        "cbs_email",
                        "photo_filename",
                        "country_of_origin",
                        "previous_employment",
                        "undergraduate_institution",
                        "desired_industry",
                        "hobbies",
                        "age",
                        "linkedin_url",
                        "consent_confirmed",
                        "consent_confirmed_at",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "full_name": "Example Student",
                        "cbs_email": "Student@Example.edu",
                        "photo_filename": "",
                        "country_of_origin": "Japan",
                        "previous_employment": "Example Health",
                        "undergraduate_institution": "Example University",
                        "desired_industry": "Healthcare",
                        "hobbies": "Running",
                        "age": "",
                        "linkedin_url": "https://www.linkedin.com/in/example-student",
                        "consent_confirmed": "true",
                        "consent_confirmed_at": "2026-09-01T10:00:00-04:00",
                    }
                )

            call_command("import_profiles", csv_path)

        profile = Profile.objects.get()
        self.assertEqual(profile.cbs_email, "student@example.edu")
        self.assertTrue(
            AuthorizedEmail.objects.filter(
                normalized_email="student@example.edu",
                is_active=True,
            ).exists()
        )
