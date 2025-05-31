# app/models.py
from datetime import datetime
from .extensions import db  # or 
#from . import db 

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)   # e.g. "Yuva", "Manmohan"
    comment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'comment': self.comment,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
