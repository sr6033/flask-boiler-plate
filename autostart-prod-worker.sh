#!/bin/bash
flask db upgrade
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program celery -A app.celery worker -c 3 --loglevel=INFO --time-limit=500 --logfile=/var/log/ind-insurance/ind-insurance-worker.log --hostname=ind-insurance &
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program celery -A app.celery worker -c 1 --loglevel=INFO --time-limit=500 -Q insurance_celery_queue_high --logfile=/var/log/ind-insurance/ind-insurance-worker.log --hostname=ind-insurance