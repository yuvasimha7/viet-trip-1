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
from app import create_app,db 


load_dotenv()



try:
    from app import create_app
except ImportError:
    create_app = None

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
        app = Flask(__name__)

        @app.route('/')
        def home():
            return render_template('index.html')

app = create_app()
with app.app_context():
    db.create_all()

# Optional: Only needed if running locally with python main.py
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)