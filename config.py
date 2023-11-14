import os

from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))
from kombu import Exchange, Queue

class Config(object):

    ENVIRONMENT = config('ENVIRONMENT', default="dev")

    # Database
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
    # SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO', default=False, cast=bool)
    # SQLALCHEMY_POOL_SIZE = 50
    # SQLALCHEMY_MAX_OVERFLOW = 1000
    DEBUG = config('FLASK_DEBUG', cast=bool, default=False)

    # AWS
    AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION', default="")
    AWS_INSURANCE_BUCKET_NAME = config('AWS_BUCKET_NAME', default="")
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default="")
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default="")
    AWS_S3_HOST = config('AWS_S3_HOST', default="")

    # Redis
    REDIS_HOST = config('REDIS_HOST', default="")
    REDIS_PORT = config('REDIS_PORT', default=6379)

    # Celery Config
    CELERY_BROKER_URL = "sqs://"
    # CELERY_BROKER_URL = "redis://localhost:6379/0"
    # CELERY_BACKEND = f"db+{config('DATABASE_URL')}"
    task_default_queue = 'default'
    broker_transport_options = {
        'region': "<AWS_REGION_NAME>",
        'visibility_timeout': 36000,
        'polling_interval': 10
    }
    task_queues = (
        Queue('high_priority', Exchange('high_priority'), routing_key='high_priority'),
        Queue('low_priority', Exchange('low_priority'), routing_key='low_priority'),
    )

    # Logging
    LOG_DIR = "/var/log/flask-boiler-plate/"
    LOG_FILE = "flask-boiler-plate-app.log"

    APP_URL = config('APP_URL', default="https://app.flask-boiler-plate.com")
    WEBVIEW_HOST = config('WEBVIEW_HOST', default="https://web.flask-boiler-plate.com")

