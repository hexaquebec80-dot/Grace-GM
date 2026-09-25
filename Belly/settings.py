from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SÉCURITÉ
# --------------------------------------------------

# Créer une NOUVELLE clé : celle de l'ancien settings.py
# a déjà été publiée dans le dépôt GitHub.
SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

# Exemple : grace-gm.onrender.com,gracegm.com,www.gracegm.com
ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default="127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]

# Render fournit ce nom automatiquement au service Web.
RENDER_EXTERNAL_HOSTNAME = config(
    "RENDER_EXTERNAL_HOSTNAME",
    default="",
)

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Exemple : https://grace-gm.onrender.com,https://gracegm.com
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config(
        "CSRF_TRUSTED_ORIGINS",
        default="",
    ).split(",")
    if origin.strip()
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{RENDER_EXTERNAL_HOSTNAME}"
    )

# Render reçoit les requêtes HTTPS derrière un proxy.
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# À activer une fois le domaine et HTTPS fonctionnels.
SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default=False,
    cast=bool,
)


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "Grace",
]

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

ROOT_URLCONF = "Belly.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "Grace.context_processors.cart_counter",
            ],
        },
    },
]

WSGI_APPLICATION = "Belly.wsgi.application"


# --------------------------------------------------
# BASE DE DONNÉES
# --------------------------------------------------

DATABASE_URL = config("DATABASE_URL", default="")

if DATABASE_URL:
    # Sur Render : DATABASE_URL de la base PostgreSQL.
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not DEBUG,
        )
    }
else:
    if not DEBUG:
        raise RuntimeError(
            "DATABASE_URL est obligatoire quand DEBUG=False. "
            "Ajoutez l'URL PostgreSQL dans les variables "
            "d'environnement de Render."
        )

    # Uniquement pour le développement local.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# --------------------------------------------------
# MOTS DE PASSE
# --------------------------------------------------

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


# --------------------------------------------------
# LANGUE ET HEURE
# --------------------------------------------------

LANGUAGE_CODE = "fr-ca"
TIME_ZONE = "America/Toronto"

USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# FICHIERS STATIQUES
# --------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Facultatif : dossier de fichiers statiques commun au projet.
# Les dossiers Belly/static et Grace/static sont déjà trouvés
# automatiquement par django.contrib.staticfiles.
if (BASE_DIR / "static").is_dir():
    STATICFILES_DIRS = [BASE_DIR / "static"]


# --------------------------------------------------
# FICHIERS TÉLÉVERSÉS
# --------------------------------------------------

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------
# STRIPE
# --------------------------------------------------

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


# --------------------------------------------------
# COURRIELS
# --------------------------------------------------

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
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


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/cart/"




# --------------------------------------------------
# CLOUDINARY
# --------------------------------------------------

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

import cloudinary

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)
