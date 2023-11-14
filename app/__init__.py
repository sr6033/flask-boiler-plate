from flask import Flask

from app.database_config import create_connector_engine
from config import Config
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from gevent import monkey
from flask_cors import CORS
from redis import Redis, BlockingConnectionPool


app = Flask(__name__)

# monkey.patch_socket()
db = SQLAlchemy()
ma = Marshmallow()


def register_blueprint(app):
    from app.urls import api_bp
    app.register_blueprint(api_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    db.create_engine = create_connector_engine(app)
    ma.init_app(app)
    # initialize_logger(app)
    return app


app = create_app()
# enable cors for externalroutes
if app.config['ENVIRONMENT'] == "dev":
    CORS(app)
# celery = make_celery(app)
redis_client = Redis(
    connection_pool=BlockingConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT']))
register_blueprint(app)
# register_commands(app)
# register_exception_handler(app)
