"""Homework Submission model"""

from app import db
from datetime import datetime


class HomeworkSubmission(db.Model):
    """Represents a homework submission from a student"""
    
    __tablename__ = 'homework_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    submission_date = db.Column(db.Date, nullable=False)
    file_path = db.Column(db.String(255))
    analysis_status = db.Column(db.String(20), default='pending')  # pending, processing, complete, failed
    total_questions = db.Column(db.Integer)
    total_mistakes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mistakes = db.relationship('Mistake', backref='submission', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<HomeworkSubmission {self.id} for Student {self.student_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'submission_date': self.submission_date.isoformat(),
            'file_path': self.file_path,
            'analysis_status': self.analysis_status,
            'total_questions': self.total_questions,
            'total_mistakes': self.total_mistakes,
            'created_at': self.created_at.isoformat()
        }
