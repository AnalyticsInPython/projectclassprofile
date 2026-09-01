# Private data import

## 1. Review before export

Confirm that each included response has explicit consent and that its required fields are complete. Remove any unapproved row before creating the import file.

## 2. Prepare local private files

Store them only under the ignored directory:

```text
data/private/
├── approved_profiles.csv
└── photos/
```

Never place real responses or photographs elsewhere in the repository.

## 3. Match the CSV schema

Use the same headers as `data/sample_profiles.csv`. Set `consent_confirmed` to `true` only after the team confirms the submitted consent. Use an ISO 8601 timestamp for `consent_confirmed_at`.

The value in `photo_filename` must be the filename only, such as `response_001.jpg`. Directory paths are rejected.

## 4. Validate without writing

```bash
uv run python manage.py import_profiles data/private/approved_profiles.csv --photo-dir data/private/photos --dry-run
```

The command rejects invalid LinkedIn URLs, invalid ages, unsupported image formats, missing photographs, malformed timestamps, and missing required columns.

## 5. Import

After validation succeeds, repeat the command without `--dry-run`. The importer creates or updates the Profile record and activates its normalized CBS email in the allowlist.

## 6. Verify and remove temporary copies

Open the application, check every card and photograph, and confirm that no email address appears on the profile page. Keep private working files only as long as the team needs them and protect any retained copy appropriately.
