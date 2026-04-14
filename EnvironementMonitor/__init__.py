import os
from flask import Flask

from . import pages

def create_app():
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=templates_path)
    app.register_blueprint(pages.bp)
    return app