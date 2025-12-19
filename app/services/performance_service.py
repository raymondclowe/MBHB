"""Performance Service - Calculates and tracks student performance metrics"""

from datetime import datetime, timedelta, date
from sqlalchemy import func
from app import db
from app.models import Student, Mistake, MistakeCategory, PerformanceMetric, HomeworkSubmission, GeneratedWorksheet


class PerformanceService:
    """Service for calculating performance metrics and trends"""
    
    @staticmethod
    def update_metrics_for_student(student_id):
        """Update all performance metrics for a student"""
        student = Student.query.get(student_id)
        if not student:
            return
        
        categories = MistakeCategory.query.filter_by(is_active=True).all()
        today = date.today()
        
        for category in categories:
            PerformanceService._calculate_category_metrics(student.id, category.id, today)
    
    @staticmethod
    def _calculate_category_metrics(student_id, category_id, metric_date):
        """Calculate metrics for a specific student-category combination"""
        # Get all mistakes for this student-category
        mistakes_query = db.session.query(Mistake).join(HomeworkSubmission).filter(
            HomeworkSubmission.student_id == student_id,
            Mistake.category_id == category_id
        )
        
        # Total occurrences
        total_occurrences = mistakes_query.count()
        
        # Recent occurrences (last 7 days)
        seven_days_ago = metric_date - timedelta(days=7)
        recent_7d = mistakes_query.filter(
            HomeworkSubmission.submission_date >= seven_days_ago
        ).count()
        
        # Recent occurrences (last 30 days)
        thirty_days_ago = metric_date - timedelta(days=30)
        recent_30d = mistakes_query.filter(
            HomeworkSubmission.submission_date >= thirty_days_ago
        ).count()
        
        # Last occurrence date
        last_mistake = mistakes_query.order_by(HomeworkSubmission.submission_date.desc()).first()
        last_occurrence_date = last_mistake.submission.submission_date if last_mistake else None
        
        # Calculate moving average (last 10 submissions)
        recent_submissions = db.session.query(
            HomeworkSubmission.id,
            HomeworkSubmission.submission_date
        ).filter(
            HomeworkSubmission.student_id == student_id
        ).order_by(
            HomeworkSubmission.submission_date.desc()
        ).limit(10).all()
        
        if recent_submissions:
            recent_mistake_counts = []
            for submission in recent_submissions:
                count = Mistake.query.filter_by(
                    submission_id=submission.id,
                    category_id=category_id
                ).count()
                recent_mistake_counts.append(count)
            
            moving_average = sum(recent_mistake_counts) / len(recent_mistake_counts)
        else:
            moving_average = 0
        
        # Determine trend
        trend = PerformanceService._calculate_trend(student_id, category_id)
        
        # Calculate priority score
        category = MistakeCategory.query.get(category_id)
        priority_score = PerformanceService._calculate_priority_score(
            recent_30d,
            category.exam_weight if category else 5,
            recent_7d > 0,
            student_id,
            category_id
        )
        
        # Create or update metric record
        metric = PerformanceMetric.query.filter_by(
            student_id=student_id,
            category_id=category_id,
            metric_date=metric_date
        ).first()
        
        if not metric:
            metric = PerformanceMetric(
                student_id=student_id,
                category_id=category_id,
                metric_date=metric_date
            )
            db.session.add(metric)
        
        metric.total_occurrences = total_occurrences
        metric.recent_occurrences_7d = recent_7d
        metric.recent_occurrences_30d = recent_30d
        metric.moving_average = moving_average
        metric.trend = trend
        metric.priority_score = priority_score
        metric.last_occurrence_date = last_occurrence_date
        
        db.session.commit()
    
    @staticmethod
    def _calculate_trend(student_id, category_id):
        """Determine if performance is improving, declining, or stable"""
        # Compare last 5 submissions to previous 5
        recent_submissions = db.session.query(
            HomeworkSubmission.id,
            HomeworkSubmission.submission_date
        ).filter(
            HomeworkSubmission.student_id == student_id
        ).order_by(
            HomeworkSubmission.submission_date.desc()
        ).limit(10).all()
        
        if len(recent_submissions) < 6:
            return 'stable'
        
        recent_5 = recent_submissions[:5]
        previous_5 = recent_submissions[5:10]
        
        recent_count = sum(
            Mistake.query.filter_by(submission_id=s.id, category_id=category_id).count()
            for s in recent_5
        )
        
        previous_count = sum(
            Mistake.query.filter_by(submission_id=s.id, category_id=category_id).count()
            for s in previous_5
        )
        
        if recent_count < previous_count * 0.7:
            return 'improving'
        elif recent_count > previous_count * 1.3:
            return 'declining'
        else:
            return 'stable'
    
    @staticmethod
    def _calculate_priority_score(frequency_30d, exam_weight, is_recent, student_id, category_id):
        """
        Calculate priority score for worksheet generation
        
        Priority Score = (Frequency × Exam Weight × Recency Factor) / Days Since Last Worksheet
        """
        if frequency_30d == 0:
            return 0
        
        # Recency factor: boost priority if mistake occurred in last 7 days
        recency_factor = 2.0 if is_recent else 1.0
        
        # Days since last worksheet
        last_worksheet = GeneratedWorksheet.query.filter_by(
            student_id=student_id,
            category_id=category_id
        ).order_by(GeneratedWorksheet.generated_at.desc()).first()
        
        if last_worksheet:
            days_since_worksheet = (datetime.utcnow() - last_worksheet.generated_at).days
            # Cap at 30 days to prevent division issues
            days_since_worksheet = max(days_since_worksheet, 1)
        else:
            days_since_worksheet = 30  # No worksheet yet, treat as 30 days
        
        priority = (frequency_30d * exam_weight * recency_factor) / days_since_worksheet
        
        return round(priority, 2)
    
    @staticmethod
    def get_top_priorities_for_student(student_id, limit=5):
        """Get top priority mistake categories for a student"""
        today = date.today()
        
        metrics = PerformanceMetric.query.filter_by(
            student_id=student_id,
            metric_date=today
        ).order_by(
            PerformanceMetric.priority_score.desc()
        ).limit(limit).all()
        
        return metrics
    
    @staticmethod
    def get_student_dashboard_data(student_id):
        """Get comprehensive dashboard data for a student"""
        student = Student.query.get(student_id)
        if not student:
            return None
        
        # Total submissions
        total_submissions = HomeworkSubmission.query.filter_by(student_id=student_id).count()
        
        # Total mistakes
        total_mistakes = db.session.query(func.sum(HomeworkSubmission.total_mistakes)).filter_by(
            student_id=student_id
        ).scalar() or 0
        
        # Recent mistakes (last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_mistakes = db.session.query(func.sum(HomeworkSubmission.total_mistakes)).filter(
            HomeworkSubmission.student_id == student_id,
            HomeworkSubmission.submission_date >= thirty_days_ago
        ).scalar() or 0
        
        # Top priorities
        top_priorities = PerformanceService.get_top_priorities_for_student(student_id, limit=5)
        
        # Recent worksheets
        recent_worksheets = GeneratedWorksheet.query.filter_by(
            student_id=student_id
        ).order_by(GeneratedWorksheet.generated_at.desc()).limit(5).all()
        
        return {
            'student': student.to_dict(),
            'total_submissions': total_submissions,
            'total_mistakes': total_mistakes,
            'recent_mistakes_30d': recent_mistakes,
            'top_priorities': [m.to_dict() for m in top_priorities],
            'recent_worksheets': [w.to_dict() for w in recent_worksheets]
        }
