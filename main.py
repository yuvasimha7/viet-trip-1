'''import os
from flask import Flask, render_template
from dotenv import load_dotenv 

load_dotenv()

try:
    from app import create_app
except ImportError:
    create_app = None

if __name__ == "__main__":
    map_path = os.path.join('static', 'map.html')

    if not os.path.exists(map_path):
        if create_app:
            app = create_app()
        else:
            raise RuntimeError("create_app() not found, but map.html is missing.")
    else:
        if create_app:
            app = create_app()
        else:
            # fallback simple app for index.html rendering only
            from flask import Flask, render_template
            app = Flask(__name__)

            @app.route('/')
            def home():
                return render_template('index.html')

    app.run(debug=True)'''




import os
from flask import Flask, render_template
from dotenv import load_dotenv 

load_dotenv()

try:
    from app import create_app
except ImportError:
    create_app = None

if __name__ == "__main__":
    if create_app:
        app = create_app()
        print("App created successfully")
    else:
        # Fallback simple app
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return render_template('index.html')
        
        print("Using fallback simple app")
    
    # Run the app
    port = int(os.environ.get("PORT", 5000))
    #debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    debug_mode=False
    print(f"Starting app on port {port}, debug={debug_mode}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)