from .base import *
import os

# Security settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')

# Allow all hosts for now - in production, you should specify exact domains
ALLOWED_HOSTS = ['*']

# For security, you should specify your exact domain in production
# ALLOWED_HOSTS = ['sr-bazaar.onrender.com', 'www.yourdomain.com']

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Fallback to SQLite if PostgreSQL is not configured
if not all([os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'), os.environ.get('DB_HOST')]):
    print("WARNING: Using SQLite as fallback. Set DB_NAME, DB_USER, DB_PASSWORD, and DB_HOST environment variables for PostgreSQL.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Print database connection info for debugging
print(f"Database engine: {DATABASES['default']['ENGINE']}")
print(f"Database name: {DATABASES['default'].get('NAME')}")
print(f"Database user: {DATABASES['default'].get('USER')}")
print(f"Database host: {DATABASES['default'].get('HOST')}")

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Razorpay settings
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')
ENABLE_PAYMENTS = os.getenv('ENABLE_PAYMENTS', 'True') == 'True'
PAYMENT_CURRENCY = os.getenv('PAYMENT_CURRENCY', 'INR')
