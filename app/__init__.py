from flask import Flask
from .routes import bp
from .map_generator import generate_map
from .suggestions import suggestions_bp  # Import new blueprint
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath("templates"))

    # Register existing blueprint (routes)
    app.register_blueprint(bp)

    # Register new suggestions blueprint (comments API)
    app.register_blueprint(suggestions_bp)

    # Ensure static folder exists and generate the map.html if needed
    os.makedirs("static", exist_ok=True)
    generate_map(os.path.join("static", "map.html"))

    return app
