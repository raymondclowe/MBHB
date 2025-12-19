"""Worksheet management routes"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from app.models import GeneratedWorksheet, Student
from app.services.worksheet_service import WorksheetService
import os

bp = Blueprint('worksheets', __name__, url_prefix='/worksheets')


@bp.route('/')
def list_worksheets():
    """List all generated worksheets"""
    worksheets = GeneratedWorksheet.query.order_by(
        GeneratedWorksheet.generated_at.desc()
    ).limit(100).all()
    
    return render_template('worksheets/list.html', worksheets=worksheets)


@bp.route('/generate/<int:student_id>/<int:category_id>', methods=['POST'])
def generate(student_id, category_id):
    """Generate a worksheet for student and category"""
    result = WorksheetService.generate_worksheet_for_category(student_id, category_id)
    
    if result['success']:
        flash('Worksheet generated successfully', 'success')
    else:
        flash(f'Error generating worksheet: {result.get("error")}', 'error')
    
    return redirect(url_for('students.view_student', student_id=student_id))


@bp.route('/download/<int:worksheet_id>')
def download(worksheet_id):
    """Download a generated worksheet"""
    worksheet = GeneratedWorksheet.query.get_or_404(worksheet_id)
    
    if os.path.exists(worksheet.file_path):
        return send_file(worksheet.file_path, as_attachment=True)
    else:
        flash('Worksheet file not found', 'error')
        return redirect(url_for('worksheets.list_worksheets'))
