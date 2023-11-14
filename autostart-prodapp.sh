#!/bin/bash
flask db upgrade
/etc/init.d/nginx start &
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn
