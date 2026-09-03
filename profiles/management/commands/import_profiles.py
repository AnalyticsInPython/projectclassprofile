import csv
from datetime import datetime
from io import BytesIO
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from PIL import Image, ImageOps, UnidentifiedImageError

from access_control.models import AuthorizedEmail
from access_control.services import normalize_email
from profiles.models import Profile


TRUE_VALUES = {"1", "true", "yes", "y"}
REQUIRED_COLUMNS = {
    "full_name",
    "cbs_email",
    "photo_filename",
    "country_of_origin",
    "previous_employment",
    "desired_industry",
    "hobbies",
    "linkedin_url",
}


class Command(BaseCommand):
    help = "Import approved Google Form profile responses from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=Path)
        parser.add_argument(
            "--photo-dir",
            type=Path,
            help="Directory containing photographs referenced by photo_filename.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate every row without changing the database or media files.",
        )

    def handle(self, *args, **options):
        csv_path = options["csv_path"].expanduser().resolve()
        photo_dir = (
            options["photo_dir"].expanduser().resolve()
            if options["photo_dir"]
            else None
        )

        if not csv_path.is_file():
            raise CommandError(f"CSV file not found: {csv_path}")
        if photo_dir and not photo_dir.is_dir():
            raise CommandError(f"Photo directory not found: {photo_dir}")

        imported = 0
        skipped = 0
        failed = 0

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - fieldnames
            if missing:
                raise CommandError(
                    "CSV is missing required columns: " + ", ".join(sorted(missing))
                )

            for row_number, row in enumerate(reader, start=2):
                consent = (row.get("consent_confirmed") or "").strip().lower()
                if "consent_confirmed" in fieldnames and consent not in TRUE_VALUES:
                    skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Row {row_number}: skipped because consent is not confirmed."
                        )
                    )
                    continue

                try:
                    profile_data = self._profile_data(row)
                    self._validate_profile_data(profile_data)
                    photo_path = self._photo_path(row, photo_dir)
                    if photo_path:
                        self._validate_photo(photo_path)

                    if not options["dry_run"]:
                        self._save_profile(profile_data, photo_path)
                    imported += 1
                except (ValueError, ValidationError, OSError) as exc:
                    failed += 1
                    self.stderr.write(
                        self.style.ERROR(f"Row {row_number}: {exc}")
                    )

        mode = "validated" if options["dry_run"] else "imported"
        self.stdout.write(
            self.style.SUCCESS(
                f"{imported} {mode}; {skipped} skipped; {failed} failed."
            )
        )
        if failed:
            raise CommandError("One or more rows failed validation.")

    def _profile_data(self, row):
        email = normalize_email(row["cbs_email"])
        if not email:
            raise ValueError("CBS email is required.")

        age_text = (row.get("age") or "").strip()
        age = int(age_text) if age_text else None

        timestamp_text = (row.get("consent_confirmed_at") or "").strip()
        timestamp = parse_datetime(timestamp_text) if timestamp_text else timezone.now()
        if timestamp and timezone.is_naive(timestamp):
            timestamp = timezone.make_aware(timestamp)
        if not timestamp:
            raise ValueError("consent_confirmed_at must be an ISO 8601 datetime.")

        return {
            "full_name": row["full_name"].strip(),
            "cbs_email": email,
            "country_of_origin": row["country_of_origin"].strip(),
            "previous_employment": row["previous_employment"].strip(),
            "undergraduate_institution": (
                row.get("undergraduate_institution") or ""
            ).strip(),
            "desired_industry": row["desired_industry"].strip(),
            "hobbies": row["hobbies"].strip(),
            "age": age,
            "linkedin_url": row["linkedin_url"].strip(),
            "consent_confirmed_at": timestamp,
        }

    def _validate_profile_data(self, profile_data):
        candidate = Profile(**profile_data)
        candidate.full_clean(validate_unique=False)

    def _photo_path(self, row, photo_dir):
        filename = Path(row["photo_filename"].strip()).name
        if not filename:
            return None
        if not photo_dir:
            raise ValueError("--photo-dir is required when photo_filename is set.")
        path = (photo_dir / filename).resolve()
        if path.parent != photo_dir:
            raise ValueError("Photo filename must not include a directory path.")
        if not path.is_file():
            raise ValueError(f"Photo file not found: {filename}")
        return path

    def _validate_photo(self, photo_path):
        try:
            with Image.open(photo_path) as image:
                image.verify()
                if image.format not in {"JPEG", "MPO", "PNG", "WEBP"}:
                    raise ValueError("Photo must be JPEG, MPO, PNG, or WebP.")
        except UnidentifiedImageError as exc:
            raise ValueError("Photo is not a valid image.") from exc

    @transaction.atomic
    def _save_profile(self, profile_data, photo_path):
        email = profile_data["cbs_email"]
        profile, _ = Profile.objects.update_or_create(
            cbs_email=email,
            defaults=profile_data,
        )
        profile.full_clean()

        if photo_path:
            if profile.photo:
                profile.photo.delete(save=False)

            with Image.open(photo_path) as image:
                photo_format = image.format

            if photo_format == "MPO":
                with Image.open(photo_path) as image:
                    image.seek(0)
                    frame = ImageOps.exif_transpose(image).convert("RGB")
                    output = BytesIO()
                    frame.save(output, format="JPEG", quality=90, optimize=True)
                profile.photo.save(
                    f"{photo_path.stem}.jpg",
                    ContentFile(output.getvalue()),
                    save=False,
                )
            else:
                with photo_path.open("rb") as handle:
                    profile.photo.save(photo_path.name, File(handle), save=False)
        profile.save()

        AuthorizedEmail.objects.update_or_create(
            normalized_email=email,
            defaults={"is_active": True},
        )
