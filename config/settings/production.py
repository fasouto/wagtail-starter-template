from .base import *  # noqa: F403
from .base import env

DEBUG = False

# SECRET_KEY has a build-time fallback so collectstatic can run during
# the Docker/Railpack build phase (before env vars are injected).
# At runtime the real key is always required via the environment variable.
SECRET_KEY = env("SECRET_KEY", default="build-time-placeholder")

DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///placeholder"),
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[".railway.app"])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# WAGTAIL
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL", default="https://your-domain.railway.app")

# SECURITY
# Railway terminates SSL at the proxy; internal traffic is HTTP.
# Let the proxy handle HTTPS redirection, not Django.
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# MEDIA STORAGE (S3/R2)
# Uncomment and configure for persistent media in production.
# pip install django-storages[s3] and add "storages" to INSTALLED_APPS.
#
# STORAGES = {
#     **STORAGES,  # noqa: F405
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#     },
# }
# AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="auto")
# AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="")
# AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default="")
# AWS_S3_FILE_OVERWRITE = False  # Required for Wagtail
