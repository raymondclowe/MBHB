"""API routes for JSON endpoints"""

from flask import Blueprint, jsonify, request
from app.models import Student, MistakeCategory
from app.services import AnalysisService, PerformanceService, WorksheetService

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/students')
def list_students():
    """API: List all students"""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@bp.route('/students/<int:student_id>')
def get_student(student_id):
    """API: Get student details"""
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())


@bp.route('/students/<int:student_id>/dashboard')
def student_dashboard(student_id):
    """API: Get student dashboard data"""
    data = PerformanceService.get_student_dashboard_data(student_id)
    if not data:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(data)


@bp.route('/categories')
def list_categories():
    """API: List all categories"""
    categories = MistakeCategory.query.filter_by(is_active=True).all()
    return jsonify([c.to_dict() for c in categories])


@bp.route('/worksheets/generate', methods=['POST'])
def generate_worksheet():
    """API: Generate a worksheet"""
    data = request.json
    student_id = data.get('student_id')
    category_id = data.get('category_id')
    
    if not student_id or not category_id:
        return jsonify({'error': 'Missing student_id or category_id'}), 400
    
    result = WorksheetService.generate_worksheet_for_category(student_id, category_id)
    return jsonify(result)


@bp.route('/analyze', methods=['POST'])
def trigger_analysis():
    """API: Trigger manual analysis of a file"""
    data = request.json
    file_path = data.get('file_path')
    
    if not file_path:
        return jsonify({'error': 'Missing file_path'}), 400
    
    result = AnalysisService.process_json_submission(file_path)
    return jsonify(result)
