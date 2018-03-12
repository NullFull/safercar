import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-y8__i2!z((_zu(z@-*u@on0vu7*(8(53x*apbbc69m6__ytn1'

MODE = os.environ.get('MODE', 'development')
DEBUG = MODE == 'development'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'desucar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'desucar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'desucar.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = '//storage.googleapis.com/newstapa-apps.appspot.com/desucar/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

NORMALIZE_MAP_PATH = os.path.join(BASE_DIR, 'data', 'normalize_map.json')

GSPREAD_AUTH = {
    "type": "service_account",
    "project_id": "newstapa-web",
    "private_key_id": "097a038b83cbfeb0fbd673670852d07299ea13b1",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDhgGMD/YbwqZ9r\n2YQtkHVI59iiRjqXrQBa4xLlmDqEQOYX9OH5FDHCQ37Zdg9rFlmieKTqI/4n0gqw\nqw/imARRoSzFVEJDrn3WytDLKrYI4KlTu1eWw0bf7Ie2i4Z4EwlwbS53ZhRptf58\nYGFVg5r2OrloCKwjGaxxtJ1c8BKc/5fLvEIiZ2SxitHtr5Ao9mpH1cqgIv0kkS2o\nkfZE0phQ9p/SSE0YqpsEfrIbY0XRthDWpvlI4RUGAtJ5G999/5k9Gb2JLorVb/xC\ntJRtcP++ly2WbCvu8RJ95C3zoGZNJf9NiFzka1hm32P8FFNVc8t8TPwjVw1h+tev\nDo6ibmP/AgMBAAECggEAKrkYyVpAtRrl7dh9nuZWGjR2yjPVCQSJYy7PVzlyqLjk\n/xfxsi+dx8ji4Q9pl2faHpqN4CBmmCPGy7b1IQCdHNwU7+PpVApcpBOz4DIc3+y0\nl/0P+KvRoz4cbjzcAqbUrHy7B3sLFgYZi3X1Ku7uroTsuKWf+1xzW+2UvNVtKVo2\nOjg4CMNWhsGPeGejjVbiUt3Ua49Nvx61XooCEAMXqDxBpunAi08oWVmz8qEo4X5Y\nnqLxAbgUxYcraHyzmR62+Ha6d2nmvV1xQ2OQHAfs1ONcxwaIWTOoeyjrLvU1ooCw\nPJu2XXf480Ri4L4IYNobsEZ4isTOefxEs42+f4IYXQKBgQD9uEFeoa5CbkVQ6B9S\nbA9PAiGvGinvFAM7st2mVrA9HaS1sG2aR19FokbvWcYzTETNrVBu9gpHmjsK4c7/\nn0qlKd6sdA78l1GoVXLPUCVQl9wMkXxi2xfiy+nnkF5ros1nAbLSEyUq5Ke/2Ufm\n1PthMxr62cyt3JuGAf3e15A8OwKBgQDjhzVcSCaZAjXhoxnquzvqCC/5ECX0O3NZ\nN/Od6pWy2ZfqAUpit2eQ9VrrC/q/r7bi1fgRI7xuu1sQTndF6SdRbbJ8bP+tbokS\nzyX3jcO+eV+FYN1dufxjJogeKkMhwJNcXVw6ZPEPJOUDO4gFpHLWVeR/F3k20Ml0\ni1XwyN2vDQKBgA8EY+IdAbpu2m1yf8AaI0HS53l8u/Spo5NZ/+KDiQTlB0W1vpb+\nGHZ/p2EtWBzbK8tcscEPkQYx68K2INFidUGXW9WrPOPYdP3YqOX6YWsGwgCAb/NN\n8nj7Bsos8lm+lhe9sv7aIT4LsJ4bVzUjcAmNw9ALKiE0SIRDA+q3qZLXAoGBAJJs\nsSpyRGSzx3kuPb+SPzydiEIA4mwK1nDUUTOPhEdVQS6XJgfhgAUJ4TjivLwfmNLi\nYIKnPN0GNdSIqrmTEnqU3gi1HNXADPbN2OE3moE6Gv77F3r59jLY2UCQciOGi08l\nxfTOgVP9qmQqK5919XF6VVJ1CMz+EKewA96xZfkBAoGAahiYbZCDxkrg+q539UT9\nLwjVM7kWGrwutkfbu8R8EWpbVtvPq4sXjw+5tJ/duZ+AeZZ0B6LUlPvHiWvzwyUk\n+Pd2NWnuScADxBrzRQICjCqBazGgvd0TX5pHG2AGrQ7uOpj100zkgrXK5vpa0FQH\nc+M9s8s64I6zakZpYdoBmtE=\n-----END PRIVATE KEY-----\n",
    "client_email": "desucar@newstapa-web.iam.gserviceaccount.com",
    "client_id": "106258591043222208812",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/desucar%40newstapa-web.iam.gserviceaccount.com"
}