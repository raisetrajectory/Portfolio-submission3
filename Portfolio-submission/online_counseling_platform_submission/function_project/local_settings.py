DEBUG = True #Visual Studio Codeで制作している場合はDEBUG = Trueに設定しましょう！
# DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com', 'Portfoliosubmission3.pythonanywhere.com']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com', 'uchiyamatakuro.pythonanywhere.com'] #ユーザー名【uchiyamatakuro】
# ALLOWED_HOSTS = ['uchiyamatakuro.pythonanywhere.com']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-cw&h(&866t*h$ns35@(6ifum4*9fcn%20ibdi0@_1_sp8ne@wi"

# from pathlib import Path
# import os

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
# STATIC_DIR = os.path.join(BASE_DIR, 'static')

# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# from django.core.management.utils import get_random_secret_key
# SECRET_KEY = get_random_secret_key()