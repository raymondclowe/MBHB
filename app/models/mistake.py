"""Mistake model"""

from app import db
from datetime import datetime


class Mistake(db.Model):
    """Represents an individual mistake made by a student"""
    
    __tablename__ = 'mistakes'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('homework_submissions.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('mistake_categories.id'), nullable=False, index=True)
    question_number = db.Column(db.Integer)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # low, medium, high
    student_answer = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Mistake {self.id} in Submission {self.submission_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'submission_id': self.submission_id,
            'category_id': self.category_id,
            'question_number': self.question_number,
            'description': self.description,
            'severity': self.severity,
            'student_answer': self.student_answer,
            'correct_answer': self.correct_answer,
            'created_at': self.created_at.isoformat()
        }
