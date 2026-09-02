# Private data import

## 1. Review before export

Confirm that each included response has explicit consent and that its required fields are complete. Remove any unapproved row before creating the import file.

## 2. Prepare local private files

For real classmate data, store the source files outside the project and Codex workspace:

```text
private-import/
├── approved_profiles.csv
└── photos/
```

Configure the SQLite database and Django-managed photo storage with absolute paths in the private `.env` file:

```dotenv
DJANGO_DATABASE_PATH=/absolute/path/to/private/class-profile/db.sqlite3
DJANGO_MEDIA_ROOT=/absolute/path/to/private/class-profile/media
```

Create the parent directories first. Never place real responses or photographs anywhere in the repository.

## 3. Match the CSV schema

The approved CSV may contain exactly these headers:

```text
full_name,csb_email,country_of_origin,previous_employment,desired_industry,hobbies,linkedin_url,photo_filename
```

`csb_email` matches the existing approved export. The importer also accepts the correctly spelled legacy header `cbs_email`. Because this file is explicitly named and treated as an approved export, the team must verify consent before adding a row. If an optional `consent_confirmed` column is present, any row without a true value is skipped.

The legacy optional columns `undergraduate_institution`, `age`, and `consent_confirmed_at` remain supported. When the timestamp is omitted, the import time is recorded.

The value in `photo_filename` must be the filename only, such as `response_001.jpg`. Directory paths are rejected.

## 4. Validate without writing

```bash
uv run python manage.py import_profiles \
  "/absolute/path/to/private-import/approved_profiles.csv" \
  --photo-dir "/absolute/path/to/private-import/photos" \
  --dry-run
```

The command rejects invalid LinkedIn URLs, invalid ages, unsupported image formats, missing photographs, malformed timestamps, and missing required columns.

## 5. Import

After validation succeeds, repeat the command without `--dry-run`. The importer creates or updates the Profile record and activates its normalized CBS email in the allowlist.

## 6. Verify and remove temporary copies

Open the application, check every card and photograph, and confirm that no email address appears on the profile page. Keep private working files only as long as the team needs them and protect any retained copy appropriately.
