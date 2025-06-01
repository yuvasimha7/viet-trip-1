from flask import Blueprint, render_template, current_app
from .map_generator import generate_map 
import os 

bp = Blueprint("main", __name__)

@bp.route('/')
def home():
    # Use current_app to get the proper static folder path
    static_folder = current_app.static_folder
    if not static_folder:
        static_folder = os.path.join(current_app.root_path, 'static')
    
    # Ensure static directory exists
    os.makedirs(static_folder, exist_ok=True)
    
    output_path = os.path.join(static_folder, 'map.html')
    
    # Check if map exists, if not generate it
    if not os.path.exists(output_path):
        try:
            print(f"Map not found at {output_path}, generating...")
            success = generate_map(output_path)
            if success:
                print(f"Map generated successfully at {output_path}")
            else:
                print("Failed to generate map")
        except Exception as e:
            print(f'Error generating map: {e}')
    else:
        print(f"Map already exists at {output_path}")
    
    return render_template('index.html')