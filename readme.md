<p align="center">
  <img src="config/static/img/wagtail-pony.png" alt="Wagtail Pony" width="80">
</p>

<h1 align="center">Wagtail Starter Template</h1>

A production-ready [Wagtail](https://wagtail.org/) CMS starter template for [Railway](https://railway.com).

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/wagtail-starter?referralCode=iZa9TM)

## Deploy to Railway

Click the button above to deploy this template. Railway will:

1. Create a new Wagtail web service
2. Provision a PostgreSQL database
3. Set `DATABASE_URL` and `SECRET_KEY` automatically
4. Run migrations on deploy (includes a default home page)
5. Start the application with gunicorn

Your site will be live in under a minute. Create a superuser via `railway run python manage.py createsuperuser` to access the Wagtail admin at `/admin/`.

### Environment variables

These are set automatically by Railway. Override them in your service settings if needed:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DATABASE_URL` | PostgreSQL connection string | Provided by Railway |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | Full URLs for POST requests (e.g. `https://myapp.up.railway.app`) | `[]` |
| `WAGTAIL_SITE_NAME` | Site name shown in Wagtail admin | `Wagtail Starter` |
| `WAGTAILADMIN_BASE_URL` | Full URL of the site | Your Railway URL |
| `DJANGO_SETTINGS_MODULE` | Settings module | `config.settings.production` |

**Important:** If you add a custom domain, add it to both `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` (with `https://` prefix). Without `CSRF_TRUSTED_ORIGINS`, POST requests (login, admin, forms) will return 403.

### Media storage

Railway has no persistent disk. Media uploads (images, documents) work locally but are lost on redeploy. For production, configure S3-compatible storage (AWS S3, Cloudflare R2, etc.). See the commented-out example in `config/settings/production.py`.

## Local Development

### Option A: uv (recommended)

Prerequisites: [uv](https://docs.astral.sh/uv/getting-started/installation/) (it installs Python 3.13 for you if needed)

```bash
git clone https://github.com/fasouto/wagtail-starter-template.git
cd wagtail-starter-template

# Install dependencies
uv sync --dev

# Set up environment
cp .env.example .env

# Run migrations (creates a default home page)
uv run python manage.py migrate

# Create admin user
uv run python manage.py createsuperuser

# Start development server
uv run python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000). The Wagtail admin is at [http://localhost:8000/admin/](http://localhost:8000/admin/).

```bash
# Run tests (with coverage)
uv run coverage run -m pytest && uv run coverage report

# Lint and format
uv run ruff check .
uv run ruff format .
```

The same checks run in GitHub Actions on every push and pull request.

### Option B: Docker Compose

Prerequisites: [Docker](https://docs.docker.com/get-docker/)

```bash
git clone https://github.com/fasouto/wagtail-starter-template.git
cd wagtail-starter-template

cp .env.example .env

# Start Wagtail + PostgreSQL
docker compose up

# In another terminal:
docker compose exec web uv run python manage.py migrate
docker compose exec web uv run python manage.py createsuperuser
```

Open [http://localhost:8000](http://localhost:8000). Code changes reload automatically.

## Project Structure

```
.
├── apps/
│   └── home/                # Home page app (Wagtail Page model)
│       ├── migrations/      # Includes data migration for default page
│       ├── templates/home/  # Page templates
│       ├── models.py        # HomePage model
│       └── tests.py
├── config/                  # Django project package
│   ├── settings/
│   │   ├── base.py          # Shared settings (includes Wagtail config)
│   │   ├── development.py   # Dev settings (DEBUG=True, SQLite)
│   │   └── production.py    # Production settings (Postgres, security, S3)
│   ├── static/              # Project-level static files
│   │   └── css/base.css
│   ├── templates/           # Project-level templates (base.html, error pages)
│   ├── urls.py              # URL routing (Wagtail admin, Django admin, health)
│   ├── asgi.py
│   └── wsgi.py
├── .github/
│   ├── workflows/ci.yml     # GitHub Actions: lint, checks, tests
│   └── dependabot.yml       # Weekly dependency updates (uv, actions, Docker)
├── docker-compose.yml       # Local dev with Docker (Wagtail + Postgres 17)
├── Dockerfile.dev           # Dev container
├── pyproject.toml           # Dependencies and tool config
├── railway.toml             # Railway deployment config
└── manage.py
```

## What's Included

- **[Wagtail 7.4 LTS](https://docs.wagtail.org/)**: powerful CMS built on Django, supported until November 2027
- **[Django 5.2 LTS](https://docs.djangoproject.com/en/5.2/)**: supported until April 2028
- **Python 3.13** via `.python-version`, picked up by uv, Docker, and Railway
- **[PostgreSQL](https://www.postgresql.org/)** via psycopg3, modern async-capable adapter
- **[WhiteNoise](https://whitenoise.readthedocs.io/)**: serve static files without nginx, with brotli compression
- **[django-environ](https://django-environ.readthedocs.io/)**: configure via environment variables and `.env` files
- **[Argon2](https://docs.djangoproject.com/en/5.2/topics/auth/passwords/#using-argon2-with-django)** password hashing (winner of the Password Hashing Competition)
- **Split settings** for separate development and production configurations
- **Health check** at `/health/`, returns JSON for Railway monitoring
- **[django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/)**: SQL queries, templates, cache inspection (dev only)
- **[ruff](https://docs.astral.sh/ruff/)** for linting (pyflakes, isort, pyupgrade, bugbear, flake8-django, bandit) and formatting
- **[pytest](https://docs.pytest.org/) + [pytest-django](https://pytest-django.readthedocs.io/)** for testing, with [coverage](https://coverage.readthedocs.io/)
- **GitHub Actions CI** running lint, Django system checks, migration checks, and tests
- **Dependabot** keeping Python packages, GitHub Actions, and Docker images up to date
- **Persistent database connections** in production (`CONN_MAX_AGE`, health checks)

## Customization

### Adding a new page type

Create a new model in `apps/home/models.py` or a new app:

```python
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
```

Then run `uv run python manage.py makemigrations && uv run python manage.py migrate`.

### Replacing the CSS

The included `config/static/css/base.css` is minimal and framework-free. Replace it with Bootstrap, Tailwind, or any CSS framework you prefer.

### Upgrading dependencies

Dependabot opens a weekly grouped pull request for Python packages. To upgrade manually:

```bash
uv lock --upgrade
uv sync --dev
uv run pytest
```

Both Django and Wagtail are pinned to their current LTS lines in `pyproject.toml`. Bump the constraints there when you want to move to a newer major version.

### Adding Celery

Add `celery[redis]` to your dependencies, create `config/celery.py`, and add a Redis service to your Railway project or `docker-compose.yml`.

## License

MIT. See [LICENSE](LICENSE).
