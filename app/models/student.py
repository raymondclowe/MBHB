"""Student model"""

from app import db
from datetime import datetime


class Student(db.Model):
    """Represents a student in the system"""
    
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    grade_level = db.Column(db.String(20))
    exam_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    homework_submissions = db.relationship('HomeworkSubmission', backref='student', lazy='dynamic')
    performance_metrics = db.relationship('PerformanceMetric', backref='student', lazy='dynamic')
    generated_worksheets = db.relationship('GeneratedWorksheet', backref='student', lazy='dynamic')
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'grade_level': self.grade_level,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
