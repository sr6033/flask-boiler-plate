wsgi_app = 'app:app'
bind = '0.0.0.0:8001'
accesslog = '/var/log/flask-boiler-plate/flask-boiler-plate-gunicorn.log'
errorlog = '/var/log/flask-boiler-plate/flask-boiler-plate-gunicorn.log'
workers = 5
limit_request_line = 0
limit_request_field_size = 0
worker_class = 'gevent'
