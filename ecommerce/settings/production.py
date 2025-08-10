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

# Database - Using PostgreSQL
import dj_database_url

# Get database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Parse database configuration from DATABASE_URL
# Format: postgresql://username:password@host:port/database
# Example: postgresql://srbazaar:password@dpg-xxxxx-oregon-postgres.render.com:5432/srbazaar

db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)

# Explicitly set the engine to PostgreSQL
db_config['ENGINE'] = 'django.db.backends.postgresql'

# Add connection health checks
db_config['CONN_HEALTH_CHECKS'] = True

DATABASES = {
    'default': db_config
}

# Log database connection details (for debugging - remove in production)
print(f"Connecting to database: {db_config['HOST']}")
print(f"Database name: {db_config['NAME']}")
print(f"Using user: {db_config['USER']}")

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
