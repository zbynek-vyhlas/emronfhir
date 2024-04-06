from .base import *  # noqa F403

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # '*'

CSRF_TRUSTED_ORIGINS = ["https://127.0.0.1:5173", "https://localhost:5173"]
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_AGE = 1800  # 30 minutes

# in development needed for reset password email
FRONTEND_DOMAIN = "localhost:5173"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar"]  # noqa F405

MIDDLEWARE = (
    MIDDLEWARE[:-1]  # noqa F405
    + [
        # from documentation: The order of MIDDLEWARE is important. You should include the
        # Debug Toolbar middleware as early as possible in the list. However, it must
        # come after any other middleware that
        # encodes the response’s content, such as GZipMiddleware.
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    + MIDDLEWARE[-1:]  # noqa F405
)

# debug toolbar
INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "errorlog": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": BASE_DIR / "error.log",  # noqa F405
        },
        # mail_admins is handler that sends error log messages to
        # administrators specified in ADMINS via SMTP server specified in EMAIL_HOST
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.db": {"level": "INFO"},
        "requests": {"level": "INFO"},
        "django": {
            "level": "INFO",
            "handlers": ["errorlog", "mail_admins"],
            "propagate": True,
        },
        "core.middleware": {"level": "DEBUG"},
    },
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "[%(asctime)s] %(log_color)s%(message)s",
            "datefmt": "%H:%M:%S",  # Format for the time part
        }
    },
    # default logger used for messages that do not match any specific logger
    "root": {"level": "DEBUG", "handlers": ["console"]},
}
