"""Analysis routes"""

from flask import Blueprint, render_template
from app.models import HomeworkSubmission, MistakeCategory

bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@bp.route('/')
def index():
    """Analysis queue page"""
    submissions = HomeworkSubmission.query.order_by(
        HomeworkSubmission.created_at.desc()
    ).limit(50).all()
    
    return render_template('analysis/queue.html', submissions=submissions)


@bp.route('/categories')
def categories():
    """List all mistake categories"""
    categories = MistakeCategory.query.filter_by(is_active=True).order_by(
        MistakeCategory.exam_weight.desc()
    ).all()
    
    return render_template('analysis/categories.html', categories=categories)
