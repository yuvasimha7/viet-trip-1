from flask import Blueprint, render_template 
from .map_generator import generate_map 
import os 

bp = Blueprint("main",__name__)

@bp.route('/')
def home():
    output_path = os.path.join('static','map.html')
    if not os.path.exists(output_path):
        try:
            generate_map(output_path)
        except Exception as e:
            print(f'Error generating map: {e}')
    return render_template('index.html')