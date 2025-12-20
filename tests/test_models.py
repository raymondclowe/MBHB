"""Tests for database models"""

import pytest
from datetime import datetime, date
from app import db
from app.models import (
    Student, MistakeCategory, HomeworkSubmission, 
    Mistake, PerformanceMetric, GeneratedWorksheet
)


class TestStudent:
    """Tests for Student model"""
    
    def test_create_student(self, app):
        """Test creating a student"""
        with app.app_context():
            # Use UUID to guarantee uniqueness across test runs
            import uuid
            unique_id = f'STU{str(uuid.uuid4())[:8]}'
            
            student = Student(
                student_id=unique_id,
                name='John Doe',
                email='john@example.com',
                grade_level='IB HL Year 2'
            )
            db.session.add(student)
            db.session.commit()
            
            assert student.id is not None
            assert student.student_id == unique_id
            assert student.name == 'John Doe'
    
    def test_student_to_dict(self, app, sample_student):
        """Test student serialization"""
        with app.app_context():
            student = Student.query.get(sample_student)
            data = student.to_dict()
            
            assert data['student_id'] == 'TEST001'
            assert data['name'] == 'Test Student'
            assert 'created_at' in data
    
    def test_student_relationships(self, app, sample_student):
        """Test student relationships"""
        with app.app_context():
            student = Student.query.get(sample_student)
            
            # Test homework_submissions relationship
            submission = HomeworkSubmission(
                student_id=student.id,
                submission_date=date.today(),
                analysis_status='pending'
            )
            db.session.add(submission)
            db.session.commit()
            
            assert len(list(student.homework_submissions)) == 1


class TestMistakeCategory:
    """Tests for MistakeCategory model"""
    
    def test_default_categories_exist(self, app):
        """Test that default categories are initialized"""
        with app.app_context():
            categories = MistakeCategory.query.all()
            assert len(categories) >= 15
            
            # Check specific categories
            cat001 = MistakeCategory.query.filter_by(category_id='CAT001').first()
            assert cat001 is not None
            assert cat001.name == 'Missing Negative Roots'
            assert cat001.exam_weight == 8
    
    def test_category_to_dict(self, app, sample_category):
        """Test category serialization"""
        with app.app_context():
            category = MistakeCategory.query.get(sample_category)
            data = category.to_dict()
            
            assert 'category_id' in data
            assert 'name' in data
            assert 'exam_weight' in data


class TestHomeworkSubmission:
    """Tests for HomeworkSubmission model"""
    
    def test_create_submission(self, app, sample_student):
        """Test creating a homework submission"""
        with app.app_context():
            submission = HomeworkSubmission(
                student_id=sample_student,
                submission_date=date.today(),
                file_path='/test/path.json',
                total_questions=5,
                total_mistakes=2
            )
            db.session.add(submission)
            db.session.commit()
            
            assert submission.id is not None
            assert submission.analysis_status == 'pending'
    
    def test_submission_to_dict(self, app, sample_student):
        """Test submission serialization"""
        with app.app_context():
            submission = HomeworkSubmission(
                student_id=sample_student,
                submission_date=date.today(),
                total_questions=5
            )
            db.session.add(submission)
            db.session.commit()
            
            data = submission.to_dict()
            assert data['student_id'] == sample_student
            assert data['total_questions'] == 5


class TestMistake:
    """Tests for Mistake model"""
    
    def test_create_mistake(self, app, sample_student, sample_category):
        """Test creating a mistake"""
        with app.app_context():
            submission = HomeworkSubmission(
                student_id=sample_student,
                submission_date=date.today()
            )
            db.session.add(submission)
            db.session.flush()
            
            mistake = Mistake(
                submission_id=submission.id,
                category_id=sample_category,
                question_number=1,
                description='Test mistake',
                severity='high'
            )
            db.session.add(mistake)
            db.session.commit()
            
            assert mistake.id is not None
            assert mistake.severity == 'high'


class TestPerformanceMetric:
    """Tests for PerformanceMetric model"""
    
    def test_create_metric(self, app, sample_student, sample_category):
        """Test creating a performance metric"""
        with app.app_context():
            metric = PerformanceMetric(
                student_id=sample_student,
                category_id=sample_category,
                metric_date=date.today(),
                total_occurrences=5,
                recent_occurrences_7d=2,
                recent_occurrences_30d=4,
                priority_score=15.5
            )
            db.session.add(metric)
            db.session.commit()
            
            assert metric.id is not None
            assert metric.priority_score == 15.5


class TestGeneratedWorksheet:
    """Tests for GeneratedWorksheet model"""
    
    def test_create_worksheet(self, app, sample_student, sample_category):
        """Test creating a generated worksheet"""
        with app.app_context():
            worksheet = GeneratedWorksheet(
                student_id=sample_student,
                category_id=sample_category,
                file_path='/path/to/worksheet.html',
                pre_worksheet_error_rate=0.5
            )
            db.session.add(worksheet)
            db.session.commit()
            
            assert worksheet.id is not None
            assert worksheet.status == 'generated'
    
    def test_improvement_percentage(self, app, sample_student, sample_category):
        """Test improvement percentage calculation"""
        with app.app_context():
            worksheet = GeneratedWorksheet(
                student_id=sample_student,
                category_id=sample_category,
                file_path='/path/to/worksheet.html',
                pre_worksheet_error_rate=0.5,
                post_worksheet_error_rate=0.2
            )
            db.session.add(worksheet)
            db.session.commit()
            
            improvement = worksheet.improvement_percentage
            assert improvement == 60.0  # (0.5 - 0.2) / 0.5 * 100
    
    def test_improvement_percentage_none_values(self, app, sample_student, sample_category):
        """Test improvement percentage with None values"""
        with app.app_context():
            worksheet = GeneratedWorksheet(
                student_id=sample_student,
                category_id=sample_category,
                file_path='/path/to/worksheet.html'
            )
            db.session.add(worksheet)
            db.session.commit()
            
            assert worksheet.improvement_percentage is None
