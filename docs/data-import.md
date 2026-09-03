# Private data import and database refresh

This procedure starts with a Google Forms response spreadsheet and updates a private local SQLite database without placing real responses or photographs in the repository.

## 1. Review before export

Confirm that each included response has explicit consent and that its required fields are complete. Remove any unapproved row before creating the import file.

## 2. Download the latest private source files

In the Google Sheets response spreadsheet, select **File → Download → Comma-separated values (.csv)**. Download the photographs from the Google Forms upload folder in Google Drive and extract them if Drive provides a ZIP archive.

Do not commit, attach, or paste the downloaded CSV, photographs, Drive links, real names, or email addresses into project discussions.

## 3. Prepare local private storage

Store all real source and generated data outside the cloned repository:

```text
private-class-profile/
├── import/
│   ├── approved_profiles.csv
│   └── photos/
├── database/
└── media/
```

Copy `.env.example` to `.env` inside the cloned project. Configure the private database and Django-managed photo storage with absolute paths:

```dotenv
DJANGO_DATABASE_PATH=/absolute/path/to/private-class-profile/database/db.sqlite3
DJANGO_MEDIA_ROOT=/absolute/path/to/private-class-profile/media
```

Create the directories before running migrations. Keep `.env`, real responses, photographs, SQLite, and generated media out of Git.

## 4. Prepare the approved CSV

Rename the exported Google Forms columns as follows. The exact source labels may differ if the form wording has changed.

| Google Forms response column | Application column |
|---|---|
| Timestamp | `Timestamp` |
| Full Name | `full_name` |
| GSB or CBS Email | `cbs_email` |
| Country of Origin | `country_of_origin` |
| Previous Role or Professional Background | `previous_employment` |
| Career Interests After Graduation | `desired_industry` |
| Hobbies | `hobbies` |
| LinkedIn Profile | `linkedin_url` |
| Profile Photo | `photo_filename` |

The resulting CSV must contain these application fields:

```text
full_name,cbs_email,country_of_origin,previous_employment,desired_industry,hobbies,linkedin_url,photo_filename
```

The `Timestamp` column may remain and is ignored. Other extra columns are also ignored. If an optional `consent_confirmed` column is present, a row without a true value is skipped. The legacy optional columns `undergraduate_institution`, `age`, and `consent_confirmed_at` remain supported.

Replace any Drive URL in `photo_filename` with the exact filename of the downloaded photograph, such as `response_001.heic` or `response_001.jpg`. The name, capitalization, and extension must match a file in `import/photos/`. Directory paths are rejected.

## 5. Install dependencies and initialize SQLite

From the cloned project directory, reproduce the Python environment and create or update the tables in the private SQLite file:

```bash
uv sync --python 3.13
uv run python manage.py migrate
```

`migrate` is safe to run again when the database already exists. A current database reports `No migrations to apply.`

## 6. Validate without writing

```bash
uv run python manage.py import_profiles \
  "/absolute/path/to/private-class-profile/import/approved_profiles.csv" \
  --photo-dir "/absolute/path/to/private-class-profile/import/photos" \
  --dry-run
```

The dry run performs the same field and photo validation as the real import. HEIC/HEIF, JPEG, PNG, WebP, and MPO source files are accepted. HEIC/HEIF input and the first frame of MPO input are converted to standard JPEG files during the real import; metadata is not copied.

Do not continue unless the summary reports `0 skipped; 0 failed.` Do not share error lines containing real values; share only a redacted row number and validation message when assistance is needed.

## 7. Update the private database

Run the same command without `--dry-run`:

```bash
uv run python manage.py import_profiles \
  "/absolute/path/to/private-class-profile/import/approved_profiles.csv" \
  --photo-dir "/absolute/path/to/private-class-profile/import/photos"
```

The importer uses normalized `cbs_email` as the key. It updates existing profiles, adds new profiles, replaces a stored photograph when a source photograph is supplied, and activates the email in the allowlist. A profile omitted from a later CSV is not automatically deleted.

If the command fails unexpectedly, it may have completed earlier rows before stopping. Correct the source data, repeat the dry run, and rerun the import; the upsert behavior prevents duplicate profiles with the same `cbs_email`.

## 8. Verify the result

Start the local server from a user-controlled terminal:

```bash
uv run python manage.py runserver
```

Open `http://127.0.0.1:8000/` and confirm:

- The displayed profile count matches the approved CSV.
- New and updated profiles appear once.
- Every photograph renders, including HEIC/HEIF and MPO source images.
- LinkedIn links open correctly.
- Email addresses are not displayed on profile cards.

Stop the development server with **Control-C** in its terminal.

## 9. Remove temporary source copies

Keep private working files only as long as the team needs them and protect any retained copy appropriately. Removing the source CSV or `import/photos/` does not remove data already stored in SQLite and `media/`.
