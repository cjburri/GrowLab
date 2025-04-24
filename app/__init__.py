import os
from flask import Flask
from app.server import bp
from app.models import db

def create_app():
    # __file__ lives in your_project/app/__init__.py
    pkg_root = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        static_folder=os.path.join(pkg_root, 'static'),   # <— serves app/static
        static_url_path='/static',                         # <— at URL /static
        template_folder=os.path.join(pkg_root, 'templates')
    )
    
    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(pkg_root, 'growlab.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        # Initialize with default config if none exists
        from app.models import Config
        if not Config.query.first():
            default_config = Config()
            db.session.add(default_config)
            db.session.commit()
    
    app.register_blueprint(bp)
    return app