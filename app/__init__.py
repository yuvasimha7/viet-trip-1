import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import db
from flask_migrate import Migrate

from .routes import bp
from .suggestions import suggestions_bp  # Import suggestions blueprint

migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath("templates"))

    # PostgreSQL configuration from environment variable (Railway will provide DATABASE_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the DB with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the route blueprints
    app.register_blueprint(bp)
    app.register_blueprint(suggestions_bp)

    # Ensure static directory exists (but don't generate map here)
    with app.app_context():
        static_dir = os.path.join(app.root_path, 'static')
        os.makedirs(static_dir, exist_ok=True)
        print(f"Static directory ensured at: {static_dir}")

    return app