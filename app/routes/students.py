"""Student management routes"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Student
from app.services.performance_service import PerformanceService
from datetime import datetime

bp = Blueprint('students', __name__, url_prefix='/students')


@bp.route('/')
def list_students():
    """List all students"""
    students = Student.query.order_by(Student.name).all()
    return render_template('students/list.html', students=students)


@bp.route('/<int:student_id>')
def view_student(student_id):
    """View student profile with performance metrics"""
    dashboard_data = PerformanceService.get_student_dashboard_data(student_id)
    if not dashboard_data:
        flash('Student not found', 'error')
        return redirect(url_for('students.list_students'))
    
    return render_template('students/profile.html', data=dashboard_data)


@bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add new student"""
    if request.method == 'POST':
        student = Student(
            student_id=request.form['student_id'],
            name=request.form['name'],
            email=request.form.get('email'),
            grade_level=request.form.get('grade_level')
        )
        
        if request.form.get('exam_date'):
            student.exam_date = datetime.strptime(request.form['exam_date'], '%Y-%m-%d').date()
        
        db.session.add(student)
        db.session.commit()
        
        flash(f'Student {student.name} added successfully', 'success')
        return redirect(url_for('students.view_student', student_id=student.id))
    
    return render_template('students/add.html')
