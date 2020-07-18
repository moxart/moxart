import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='secret-key-here',
        SQLALCHEMY_DATABASE_URI='mysql://moxart:password@localhost/moxart',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='jwt-secret-key-here',
        JSON_SORT_KEYS=False
    )

    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Plugins
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Include Our API Routes
        from .routes import auth
        from .routes.api import user

        # Register Blueprints
        app.register_blueprint(auth.bp)
        app.register_blueprint(user.bp)

        # Include Our Models
        from .models import user

    return app
