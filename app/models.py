from flask import Blueprint, request, jsonify
from datetime import datetime
from . import db
from .models import Comment

suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    data = request.get_json()
    category = data.get('name')  # corresponds to Comment.category
    comment_text = data.get('suggestion')  # corresponds to Comment.comment

    if not category or not comment_text:
        return jsonify({'error': 'Missing category or suggestion'}), 400

    # Create new comment record
    new_comment = Comment(
        category=category,
        comment=comment_text,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'status': 'success'})


@suggestions_bp.route('/get_suggestions')
def get_suggestions():
    category = request.args.get('name')
    if not category:
        return jsonify({'suggestions': []})

    comments = Comment.query.filter_by(category=category).order_by(Comment.timestamp.desc()).all()
    comments_list = [comment.to_dict() for comment in comments]

    return jsonify({'suggestions': comments_list})
