import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from PIL import Image

from access_control.models import AuthorizedEmail
from profiles.models import Profile


class ImportProfilesTests(TestCase):
    def test_dry_run_rejects_invalid_model_fields_before_writing(self):
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
                        "full_name": "Invalid Example",
                        "csb_email": "not-an-email",
                        "country_of_origin": "",
                        "previous_employment": "",
                        "desired_industry": "",
                        "hobbies": "",
                        "linkedin_url": "not-a-url",
                        "photo_filename": "",
                    }
                )

            with self.assertRaises(CommandError):
                call_command("import_profiles", csv_path, dry_run=True)

        self.assertFalse(Profile.objects.exists())

    def test_import_converts_mpo_to_standard_jpeg(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            photo_dir = root / "photos"
            media_dir = root / "media"
            photo_dir.mkdir()
            mpo_path = photo_dir / "portrait.jpg"
            first_frame = Image.new("RGB", (8, 8), "red")
            second_frame = Image.new("RGB", (8, 8), "blue")
            first_frame.save(
                mpo_path,
                format="MPO",
                save_all=True,
                append_images=[second_frame],
            )

            csv_path = root / "approved_profiles.csv"
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
                        "full_name": "MPO Example",
                        "csb_email": "mpo@example.edu",
                        "country_of_origin": "",
                        "previous_employment": "",
                        "desired_industry": "",
                        "hobbies": "",
                        "linkedin_url": "",
                        "photo_filename": mpo_path.name,
                    }
                )

            with override_settings(MEDIA_ROOT=media_dir):
                call_command("import_profiles", csv_path, photo_dir=photo_dir)
                call_command("import_profiles", csv_path, photo_dir=photo_dir)
                profile = Profile.objects.get(cbs_email="mpo@example.edu")
                stored_path = Path(profile.photo.path)
                self.assertEqual(stored_path.suffix, ".jpg")
                self.assertEqual(
                    len(list((media_dir / "profile_photos").iterdir())),
                    1,
                )
                with Image.open(stored_path) as stored_image:
                    self.assertEqual(stored_image.format, "JPEG")
                    self.assertEqual(getattr(stored_image, "n_frames", 1), 1)

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
