"""Mistake Category model"""

from app import db
from datetime import datetime


class MistakeCategory(db.Model):
    """Represents a category of mistakes students can make"""
    
    __tablename__ = 'mistake_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    exam_weight = db.Column(db.Integer, default=5)  # 1-10 scale
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mistakes = db.relationship('Mistake', backref='category', lazy='dynamic')
    performance_metrics = db.relationship('PerformanceMetric', backref='category', lazy='dynamic')
    generated_worksheets = db.relationship('GeneratedWorksheet', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<MistakeCategory {self.category_id}: {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'exam_weight': self.exam_weight,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
