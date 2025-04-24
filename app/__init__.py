import os
from flask import Flask
from app.server import bp

def create_app():
    # __file__ lives in your_project/app/__init__.py
    pkg_root = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        static_folder=os.path.join(pkg_root, 'static'),   # <— serves app/static
        static_url_path='/static',                         # <— at URL /static
        template_folder=os.path.join(pkg_root, 'templates')
    )
    app.register_blueprint(bp)
    return app