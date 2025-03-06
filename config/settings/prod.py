from .base import *
from .base import env

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES = {
    "default": env.db("DJANGO_DATABASE_URL", default="sqlite:///db.sqlite3"),
}
DATABASES["default"]["CONN_MAX_AGE"] = env.int(
    "DJANGO_CONN_MAX_AGE", default=60
)  # noqa: F405
DATABASES["default"]["OPTIONS"] = {
    **env.json("DJANGO_DATABASE_OPTIONS", default={})
}

# SECURITY
SECURE_PROXY_SSL_HEADER = ("DJANGO_HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)


import sentry_sdk

sentry_sdk.init(
    dsn="https://2edc96be82cc85cd69ffb8efd8f981b6@o162891.ingest.sentry.io/4506638271709184",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
