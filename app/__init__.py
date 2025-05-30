import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from .routes import bp
from .map_generator import generate_map
from .suggestions import suggestions_bp  # Import suggestions blueprint

# Initialize the SQLAlchemy object globally so it can be imported elsewhere
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath("templates"))

    # PostgreSQL configuration from environment variable (Railway will provide DATABASE_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the DB with app
    db.init_app(app)

    # Register the route blueprints
    app.register_blueprint(bp)
    app.register_blueprint(suggestions_bp)

    # Ensure 'static/' exists and generate map
    os.makedirs("static", exist_ok=True)
    generate_map(os.path.join("static", "map.html"))

    return app
