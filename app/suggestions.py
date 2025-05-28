from flask import Blueprint, request, jsonify
from datetime import datetime

suggestions_bp = Blueprint('suggestions', __name__)

# In-memory store for quick test, replace with DB for production
comments_store = {
    "Name1": [],
    "Name2": [],
    "Name3": [],
    "Name4": []
}

@suggestions_bp.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    data = request.get_json()
    name = data.get('name')
    suggestion = data.get('suggestion')
    if not name or not suggestion:
        return jsonify({'error': 'Missing name or suggestion'}), 400

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    comments_store.setdefault(name, []).append({'text': suggestion, 'time': timestamp})
    return jsonify({'status': 'success'})


@suggestions_bp.route('/get_suggestions')
def get_suggestions():
    name = request.args.get('name')
    if not name or name not in comments_store:
        return jsonify({'suggestions': []})
    return jsonify({'suggestions': comments_store[name]})
