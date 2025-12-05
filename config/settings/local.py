from .base import *  # noqa: F401, F403

DEBUG = True

# SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Console email backend - prints emails to console/logs
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Also log emails to file
EMAIL_FILE_PATH = LOGS_DIR  # noqa: F405
