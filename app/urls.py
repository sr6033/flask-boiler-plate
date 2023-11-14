from flask import Blueprint
from app.foo_bar.urls import foo_bar

api_bp = Blueprint(
    'api_bp', __name__, url_prefix="/api",
)

api_bp.register_blueprint(foo_bar)