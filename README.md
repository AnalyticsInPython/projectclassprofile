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

Install the project dependencies and create the local `.venv` with uv:

```bash
uv sync --python 3.13
```

Copy `.env.example` to `.env` and replace the placeholder values. Keep `DEBUG=true` for local use. The shared class access code belongs only in `.env`.

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

Place the reviewed CSV and photographs under the ignored `data/private/` directory. The photo names in `photo_filename` must match files in the supplied photo directory.

Run validation first:

```bash
uv run python manage.py import_profiles data/private/approved_profiles.csv --photo-dir data/private/photos --dry-run
```

If every row passes, run the same command without `--dry-run`.

See `docs/google-form.md` and `docs/data-import.md` for the required fields and review process.

## Tests

```bash
uv run python manage.py test
```
