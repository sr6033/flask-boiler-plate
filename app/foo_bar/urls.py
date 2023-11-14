from flask import Blueprint
from app.foo_bar.views import TestView

foo_bar = Blueprint(
    'foo_bar', __name__, url_prefix="/foo_bar/<version>",
)

foo_bar.add_url_rule(
    "/test",
    view_func=TestView.as_view(
        "test-class"
    ),
    methods=['GET']
)