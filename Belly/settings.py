from pathlib import Path

import cloudinary
import dj_database_url

from decouple import config


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SÉCURITÉ DJANGO
# ============================================================

SECRET_KEY = config(
    "DJANGO_SECRET_KEY",
    default="django-insecure-change-me-in-render",
)

DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool,
)


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default=(
            "127.0.0.1,"
            "localhost,"
            "gracegm.com,"
            "www.gracegm.com"
        ),
    ).split(",")
    if host.strip()
]


# Render ajoute normalement automatiquement cette variable.
RENDER_EXTERNAL_HOSTNAME = config(
    "RENDER_EXTERNAL_HOSTNAME",
    default="",
)

if (
    RENDER_EXTERNAL_HOSTNAME
    and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS
):
    ALLOWED_HOSTS.append(
        RENDER_EXTERNAL_HOSTNAME
    )


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config(
        "CSRF_TRUSTED_ORIGINS",
        default=(
            "https://gracegm.com,"
            "https://www.gracegm.com"
        ),
    ).split(",")
    if origin.strip()
]


if RENDER_EXTERNAL_HOSTNAME:
    render_origin = (
        f"https://{RENDER_EXTERNAL_HOSTNAME}"
    )

    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(
            render_origin
        )


# ============================================================
# HTTPS / RENDER
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default=False,
    cast=bool,
)


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary_storage",
    "cloudinary",

    # Application
    "Grace",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URLS / WSGI
# ============================================================

ROOT_URLCONF = "Belly.urls"

WSGI_APPLICATION = "Belly.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django."
            "DjangoTemplates"
        ),

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [

                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages."
                "context_processors.messages",

                "Grace.context_processors.cart_counter",
            ],
        },
    },
]


# ============================================================
# BASE DE DONNÉES
# ============================================================

DATABASE_URL = config(
    "DATABASE_URL",
    default="",
)


if DATABASE_URL:

    # PostgreSQL Render
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not DEBUG,
        )
    }

else:

    # En production, PostgreSQL est obligatoire.
    if not DEBUG:
        raise RuntimeError(
            "DATABASE_URL est obligatoire lorsque "
            "DEBUG=False. Ajoutez DATABASE_URL dans "
            "Render > Environment."
        )

    # Développement local seulement
    DATABASES = {
        "default": {
            "ENGINE": (
                "django.db.backends.sqlite3"
            ),
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# VALIDATION MOTS DE PASSE
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# LANGUE / DATE / HEURE
# ============================================================

LANGUAGE_CODE = "fr-ca"

TIME_ZONE = "America/Toronto"

USE_I18N = True

USE_TZ = True


# ============================================================
# CLOUDINARY
# ============================================================

CLOUDINARY_CLOUD_NAME = config(
    "CLOUDINARY_CLOUD_NAME",
    default="",
)

CLOUDINARY_API_KEY = config(
    "CLOUDINARY_API_KEY",
    default="",
)

CLOUDINARY_API_SECRET = config(
    "CLOUDINARY_API_SECRET",
    default="",
)


# Configuration django-cloudinary-storage
CLOUDINARY_STORAGE = {

    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,

    "API_KEY": CLOUDINARY_API_KEY,

    "API_SECRET": CLOUDINARY_API_SECRET,

    "SECURE": True,
}


# Configuration directe du SDK Cloudinary.
# Ceci évite notamment :
#
# ValueError: Must supply api_key
#
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)


# ============================================================
# STOCKAGE DES FICHIERS
# ============================================================

STORAGES = {

    # Images / fichiers envoyés par les utilisateurs
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage."
            "MediaCloudinaryStorage"
        ),
    },

    # CSS / JavaScript / images statiques
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================
# FICHIERS STATIQUES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)


# Dossier static global facultatif
if (BASE_DIR / "static").is_dir():

    STATICFILES_DIRS = [
        BASE_DIR / "static"
    ]


# ============================================================
# MEDIA
# ============================================================

MEDIA_URL = "/media/"


# MEDIA_ROOT n'est pas réellement utilisé en production
# lorsque Cloudinary est le stockage par défaut.
#
# Il reste utile en développement ou pour certains scripts.
MEDIA_ROOT = (
    BASE_DIR / "media"
)


# ============================================================
# TYPE DE CLÉ PRIMAIRE
# ============================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# ============================================================
# STRIPE
# ============================================================

STRIPE_PUBLIC_KEY = config(
    "STRIPE_PUBLIC_KEY",
    default="",
)

STRIPE_SECRET_KEY = config(
    "STRIPE_SECRET_KEY",
    default="",
)

STRIPE_WEBHOOK_SECRET = config(
    "STRIPE_WEBHOOK_SECRET",
    default="",
)


# ============================================================
# COURRIELS
# ============================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp."
    "EmailBackend"
)

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False


EMAIL_HOST_USER = config(
    "EMAIL_HOST_USER",
    default="",
)


EMAIL_HOST_PASSWORD = config(
    "EMAIL_HOST_PASSWORD",
    default="",
)


DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default=EMAIL_HOST_USER,
)


# Timeout afin d'éviter qu'une connexion SMTP
# bloque trop longtemps le serveur.
EMAIL_TIMEOUT = 20


# ============================================================
# CONNEXION UTILISATEUR
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "/cart/"


# Facultatif :
# LOGIN_REDIRECT_URL peut être remplacé par
# une URL Django nommée dans les vues.


# ============================================================
# SESSIONS
# ============================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False

SESSION_SAVE_EVERY_REQUEST = False


# ============================================================
# SÉCURITÉ HTTP
# ============================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# ============================================================
# LOGGING
# ============================================================

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "verbose": {

            "format": (
                "{levelname} "
                "{asctime} "
                "{name} "
                "{message}"
            ),

            "style": "{",
        },

    },

    "handlers": {

        "console": {

            "class": (
                "logging.StreamHandler"
            ),

            "formatter": "verbose",
        },

    },

    "loggers": {

        "django": {

            "handlers": [
                "console"
            ],

            "level": "INFO",

            "propagate": False,
        },

        "django.request": {

            "handlers": [
                "console"
            ],

            "level": "ERROR",

            "propagate": False,
        },

    },
}