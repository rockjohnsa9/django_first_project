import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATIC_URL = '/staticfiles/'

MEDIA_ROOT = os.path.join(STATIC_URL, 'images')
MEDIA_URL = '/'

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
