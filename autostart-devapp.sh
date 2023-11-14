#!/bin/bash
#NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program flask run

celery -A app.celery beat --loglevel=INFO --logfile=/var/log/ind-insurance/ind-insurance-gunicorn.log &
celery -A app.celery worker -c 2 --loglevel=INFO --time-limit=500 --logfile=/var/log/ind-insurance/ind-insurance-gunicorn.log --hostname=ind-insurance &
gunicorn