"""Common settings and globals."""

from os.path import abspath, basename, dirname, join, normpath, isdir
from sys import path, stdout
from tb_website import environment

MOD_VERSION = '0.6.0'
MOD_PACKAGE = 'gentb'

########## ADMIN CONFIGURATION
# Administrators for the site
# See https://docs.djangoproject.com/en/2.2/ref/settings/#admins
ADMINS = [tuple(a.split(':')) for a in environment.get_list('GENTB_ADMINS', default=[])]
TB_ADMINS = ADMINS
########## END ADMIN CONFIGURATION

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = normpath(join(abspath(__file__), '..'))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Absolute path where all data (media, datasets, etc) should go:
DATA_ROOT = environment.get_str('GENTB_SHARED_ROOT', '/mnt/gentb')

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION

########## SECRET CONFIGURATION
SECRET_KEY = environment.get_str('GENTB_SECRET_KEY', required=True)

# linked to a Dropbox app for retrieving files from shared links
# see This functionality uses the Dropbox Core API to retrieve metadata from a shared link.
#    https://blogs.dropbox.com/developers/2015/08/new-api-endpoint-shared-link-metadata/
DROPBOX_ACCESS_TOKEN = environment.get_str('GENTB_DROPBOX_ACCESS_TOKEN', required=True)
DROPBOX_APP_KEY = environment.get_str('GENTB_DROPBOX_APP_KEY', required=True)
########## END SECRET CONFIGURATION

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = environment.get_bool('GENTB_DEBUG', default=False)
########## END DEBUG CONFIGURATION

########## ADDRESS CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = environment.get_list('ALLOWED_HOSTS', required=True)
#IS_HTTPS_SITE = environment.get_list('IS_HTTPS_SITE', default=True)

# Callback url when pipeline is complete
INTERNAL_CALLBACK_SITE_URL = ''

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END ADDRESS CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend
EMAIL_BACKEND = environment.get_str('GENTB_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = environment.get_str('GENTB_EMAIL_HOST', default='')
EMAIL_PORT = environment.get_int('GENTB_EMAIL_PORT', default=587)
EMAIL_HOST_USER = environment.get_str('GENTB_EMAIL_USER', default='')
EMAIL_HOST_PASSWORD = environment.get_str('GENTB_EMAIL_PASSWORD', default='')
DEFAULT_FROM_EMAIL = environment.get_str('GENTB_EMAIL_FROM', default='admin@gentb.hms.harvard.edu')
EMAIL_USE_TLS = True
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': environment.get_str('GENTB_DB_ENGINE', default='django.contrib.gis.db.backends.postgis'),
        'NAME': environment.get_str('GENTB_DB_NAME', default='gentb'),
        'USER': environment.get_str('GENTB_DB_USER', default='gentb'),
        'PASSWORD': environment.get_str('GENTB_DB_PASSWORD'),
        'HOST': environment.get_str('GENTB_DB_HOST'),
        'PORT': environment.get_str('GENTB_DB_PORT', default='3306'),
        #'OPTIONS':  "SET sql_mode='STRICT_TRANS_TABLES';",
    }
}
########## END DATABASE CONFIGURATION

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#time-zone
TIME_ZONE = 'America/New_York'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#use-i18n
USE_I18N = False

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#use-tz
USE_TZ = True

FORMAT_MODULE_PATH = [
    'tb_website.formats',
]
########## END GENERAL CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION

########## PIPELINE/CHORE CONFIGURATION
# Location where datasets are stored
TB_SHARED_DATAFILE_DIRECTORY = normpath(join(DATA_ROOT, 'data'))

PIPELINE_MODULE = environment.get_str('GENTB_PIPELINE_MODULE', default='chore.shell.BatchJobManager')
PIPELINE_BATCHED = environment.get_str('PIPELINE_BATCHED', default=False)
PIPELINE_ROOT = normpath(join(DATA_ROOT, 'pipeline'))
PIPELINE_BIN = normpath(join(DATA_ROOT, 'bin'))

# Define the pipeline and job description to use
GENTB_PIPELINE_TEST = environment.get_bool('GENTB_PIPELINE_TEST', default=False)
GENTB_PIPELINE_JOB_QUEUE = environment.get_str('GENTB_PIPELINE_JOB_QUEUE', required=True)
GENTB_PIPELINE_JOB_DEFINITION = environment.get_str('GENTB_PIPELINE_JOB_DEFINITION', required=True)

########## END PIPELINE/CHORE CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#media-root
MEDIA_ROOT = join(normpath(DATA_ROOT), '')

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#media-url
MEDIA_URL = join(normpath(environment.get_str('DBMI_APP_MEDIA_URL_PATH', required=True)), '')

# Set file storage configuration here
DEFAULT_FILE_STORAGE = environment.get_str('GENTB_FILE_STORAGE', default='django.core.files.storage.FileSystemStorage')

########## END MEDIA CONFIGURATION

########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#static-root
STATIC_ROOT = join(normpath(environment.get_str('DBMI_APP_STATIC_ROOT', required=True)), '')

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#static-url
STATIC_URL = join(normpath(environment.get_str('DBMI_APP_STATIC_URL_PATH', required=True)), '')

# Used by resumable to store upload chunks before reconstruction
UPLOAD_ROOT = normpath(join(DATA_ROOT, 'upload'))
UPLOAD_CACHE_ROOT = join(UPLOAD_ROOT, 'url_caches')

# See: https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
# Should only contain static files not included in apps
STATICFILES_DIRS = []

# See: https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION

########## TEMPLATE CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
          normpath(join(SITE_ROOT, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
########## END TEMPLATE CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#middleware-classes
MIDDLEWARE = [
    # Default Django middleware.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # App based middleware
    #'tb_website.middleware.AutoBreadcrumbMiddleware',
    # Support Middleware
    #'apps.versioner.middleware.VersionInformation',
]

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = '/'
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
)

# Apps from the internet (see requirements.txt)
WEBSITE_APPS = (
    'django_media_fixtures',
    'django.contrib.gis',
    'django_spaghetti',
    'adminsortable2',
    #'apps.versioner',

    # Holds dataverse file ids for Two Ravens
    'apps.explore',

    # Healthchecks
    'health_check',
    'health_check.db',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'tb_website',
    'apps.tb_users',
    'apps.predict',
    'apps.pipeline.app.PipelineApp',
    'apps.uploads',
    'apps.mutations',
    'apps.maps',
)

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#installed-apps
INSTALLED_APPS = LOCAL_APPS + DJANGO_APPS + WEBSITE_APPS
########## END APP CONFIGURATION

########## DEBUG CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/js/jquery.min.js',
}
########## END DEBUG CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/1.11/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': stdout,
        },
    },
    'loggers': {
        # Default for all modules
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'WARNING',
        },
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'apps': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'chore': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}

########## END LOGGING CONFIGURATION

SPAGHETTI_SAUCE = {
  'apps': ['mutations', 'maps', 'predict', 'pipeline', 'uploads'],
  'show_fields': False,
  'exclude': {'auth': ['user']}
}

VERSION_BRANCHES = [
    ('Incoming', 'master')
]
