"""Performance Metric model"""

from app import db
from datetime import datetime


class PerformanceMetric(db.Model):
    """Tracks student performance metrics for mistake categories"""
    
    __tablename__ = 'performance_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('mistake_categories.id'), nullable=False, index=True)
    metric_date = db.Column(db.Date, nullable=False)
    total_occurrences = db.Column(db.Integer, default=0)
    recent_occurrences_7d = db.Column(db.Integer, default=0)
    recent_occurrences_30d = db.Column(db.Integer, default=0)
    moving_average = db.Column(db.Float)
    trend = db.Column(db.String(20))  # improving, declining, stable
    priority_score = db.Column(db.Float)
    last_occurrence_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite index for efficient queries
    __table_args__ = (
        db.Index('idx_student_category_date', 'student_id', 'category_id', 'metric_date'),
    )
    
    def __repr__(self):
        return f'<PerformanceMetric Student:{self.student_id} Category:{self.category_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'category_id': self.category_id,
            'metric_date': self.metric_date.isoformat(),
            'total_occurrences': self.total_occurrences,
            'recent_occurrences_7d': self.recent_occurrences_7d,
            'recent_occurrences_30d': self.recent_occurrences_30d,
            'moving_average': self.moving_average,
            'trend': self.trend,
            'priority_score': self.priority_score,
            'last_occurrence_date': self.last_occurrence_date.isoformat() if self.last_occurrence_date else None,
            'created_at': self.created_at.isoformat()
        }
