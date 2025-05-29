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
        
        # Initialize with default event codes if none exist
        from app.models import Event
        if not Event.query.first():
            default_events = [
                Event(id=100, event_string="Light off"),
                Event(id=101, event_string="Light on"),
                Event(id=200, event_string="Atomizer off"),
                Event(id=201, event_string="Atomizer on"),
                Event(id=300, event_string="Fan off"),
                Event(id=301, event_string="Fan on"),
                Event(id=400, event_string="Pump off"),
                Event(id=401, event_string="Pump on"),
                Event(id=500, event_string="Heater off"),
                Event(id=501, event_string="Heater on")
            ]
            for event in default_events:
                db.session.add(event)
            db.session.commit()
    
    app.register_blueprint(bp)
    return app