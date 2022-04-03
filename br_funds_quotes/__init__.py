from flask import Flask
from .quotes.quotes_blueprint import funds_quotes_blueprint
from .root_blueprint import root_blueprint
import os

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    app.register_blueprint(root_blueprint)
    app.register_blueprint(funds_quotes_blueprint)

    return app