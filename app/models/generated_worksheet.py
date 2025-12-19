"""Generated Worksheet model"""

from app import db
from datetime import datetime


class GeneratedWorksheet(db.Model):
    """Tracks worksheets generated for students"""
    
    __tablename__ = 'generated_worksheets'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('mistake_categories.id'), nullable=False, index=True)
    file_path = db.Column(db.String(255), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='generated')  # generated, assigned, completed
    pre_worksheet_error_rate = db.Column(db.Float)
    post_worksheet_error_rate = db.Column(db.Float)
    
    def __repr__(self):
        return f'<GeneratedWorksheet {self.id} for Student {self.student_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'category_id': self.category_id,
            'file_path': self.file_path,
            'generated_at': self.generated_at.isoformat(),
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'pre_worksheet_error_rate': self.pre_worksheet_error_rate,
            'post_worksheet_error_rate': self.post_worksheet_error_rate
        }
    
    @property
    def improvement_percentage(self):
        """Calculate improvement percentage if both rates are available"""
        if self.pre_worksheet_error_rate and self.post_worksheet_error_rate:
            if self.pre_worksheet_error_rate == 0:
                return 0
            return ((self.pre_worksheet_error_rate - self.post_worksheet_error_rate) / 
                   self.pre_worksheet_error_rate * 100)
        return None
