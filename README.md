# MBAxMS Class Profile Directory

A local Django application for learning classmates' names, faces, backgrounds, and career interests. The application is designed for a classroom MVP and is not deployed publicly.

## Privacy boundary

The GitHub repository may contain application code, documentation, the neutral placeholder image, and fictional sample data only.

Never commit:

- Real Google Form responses
- CBS email addresses
- Classmate photographs
- `db.sqlite3`
- `.env` or the shared access code
- Files under `media/` or `data/private/`

These paths are excluded by `.gitignore`.

## Local setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd <cloned-project-directory>
```

Install the project dependencies and create the local `.venv` with uv:

```bash
uv sync --python 3.13
```

Create the private local environment file, then replace its placeholder values. Never paste its contents into an issue, chat, or commit.

```bash
cp .env.example .env
```

Keep `DEBUG=true` for local use. The shared class access code belongs only in `.env`.

Login protection is disabled by default for the classroom development phase. Set `REQUIRE_CLASS_LOGIN=true` in `.env` to restore the approved-email and shared-code login before exposing the server beyond a trusted local development environment.

To keep the real database and uploaded photographs outside the project directory, add absolute paths to the private `.env` file:

```dotenv
DJANGO_DATABASE_PATH=/absolute/path/to/private-class-profile/database/db.sqlite3
DJANGO_MEDIA_ROOT=/absolute/path/to/private-class-profile/media
```

Create both parent directories before running migrations. Do not put these private paths or files in Git. If the variables are omitted, the application uses `db.sqlite3` and `media/` inside the project for fictional local development data.

Initialize the local database:

```bash
uv run python manage.py migrate
```

Validate the fictional sample without changing the database:

```bash
uv run python manage.py import_profiles data/sample_profiles.csv --dry-run
```

Import the fictional sample:

```bash
uv run python manage.py import_profiles data/sample_profiles.csv
```

Start the application:

```bash
uv run python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

The sample profiles use fictional email addresses. Add those addresses to the allowlist through the import command, then use the locally configured class access code to sign in.

## Importing approved private responses

For real data, keep the reviewed CSV and source photographs outside the project and pass their absolute paths to the import command. The photo names in `photo_filename` must match files in the supplied photo directory.

Run validation first:

```bash
uv run python manage.py import_profiles \
  "/absolute/path/to/private-class-profile/import/approved_profiles.csv" \
  --photo-dir "/absolute/path/to/private-class-profile/import/photos" \
  --dry-run
```

If every row passes, run the same command without `--dry-run`.

See `docs/google-form.md` and `docs/data-import.md` for the required fields and review process.

The import is an upsert keyed by `cbs_email`: existing profiles are updated and new profiles are added. Profiles absent from a later CSV are not automatically deleted.

## Tests

```bash
uv run python manage.py test
```
