"""Main routes - Dashboard and home"""

from flask import Blueprint, render_template
from app.models import Student, HomeworkSubmission, GeneratedWorksheet
from app.services.performance_service import PerformanceService
from sqlalchemy import func
from datetime import date, timedelta

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Dashboard home page"""
    # Summary statistics
    total_students = Student.query.count()
    total_submissions = HomeworkSubmission.query.count()
    total_worksheets = GeneratedWorksheet.query.count()
    
    # Recent activity (last 7 days)
    seven_days_ago = date.today() - timedelta(days=7)
    recent_submissions = HomeworkSubmission.query.filter(
        HomeworkSubmission.submission_date >= seven_days_ago
    ).count()
    
    # Recent students with activity
    active_students = Student.query.join(HomeworkSubmission).filter(
        HomeworkSubmission.submission_date >= seven_days_ago
    ).distinct().all()
    
    return render_template('dashboard.html',
                         total_students=total_students,
                         total_submissions=total_submissions,
                         total_worksheets=total_worksheets,
                         recent_submissions=recent_submissions,
                         active_students=active_students)


@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
