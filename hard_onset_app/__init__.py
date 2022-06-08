from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'itsadev')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    db.Model.metadata.reflect(db.engine)

    with app.app_context():
        db.init_app(app)
        from . import routes
    return app