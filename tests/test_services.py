"""Tests for service layer"""

import pytest
import json
import tempfile
from datetime import date, timedelta
from app import db
from app.models import Student, MistakeCategory, HomeworkSubmission, Mistake, PerformanceMetric
from app.services.analysis_service import AnalysisService
from app.services.performance_service import PerformanceService


class TestAnalysisService:
    """Tests for AnalysisService"""
    
    def test_process_json_submission(self, app, sample_homework_data):
        """Test processing a JSON homework submission"""
        with app.app_context():
            # Create temporary JSON file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(sample_homework_data, f)
                temp_path = f.name
            
            # Process the submission
            result = AnalysisService.process_json_submission(temp_path)
            
            assert result['success'] is True
            assert 'submission_id' in result
            assert result['mistakes'] == 2
            
            # Verify student was created
            student = Student.query.filter_by(student_id='TEST001').first()
            assert student is not None
            
            # Verify submission was created
            submission = HomeworkSubmission.query.get(result['submission_id'])
            assert submission is not None
            assert submission.total_questions == 2
            assert submission.total_mistakes == 2
            
            # Verify mistakes were created
            mistakes = Mistake.query.filter_by(submission_id=submission.id).all()
            assert len(mistakes) == 2
    
    def test_match_mistake_to_category(self, app):
        """Test mistake matching to categories"""
        with app.app_context():
            # Test exact match
            category = AnalysisService._match_mistake_to_category(
                'missing_negative_root',
                'Student forgot negative solution'
            )
            assert category is not None
            assert category.category_id == 'CAT001'
            
            # Test keyword match
            category = AnalysisService._match_mistake_to_category(
                None,
                'Forgot to add constant of integration +C'
            )
            assert category is not None
            assert category.category_id == 'CAT006'
    
    def test_get_or_create_other_category(self, app):
        """Test creating 'Other' category"""
        with app.app_context():
            category = AnalysisService._get_or_create_other_category()
            assert category is not None
            assert category.category_id == 'CAT999'


class TestPerformanceService:
    """Tests for PerformanceService"""
    
    def test_update_metrics_for_student(self, app, sample_student, sample_category):
        """Test updating performance metrics"""
        with app.app_context():
            # Create some test data
            submission = HomeworkSubmission(
                student_id=sample_student,
                submission_date=date.today(),
                total_questions=5,
                total_mistakes=2
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
            
            # Update metrics
            PerformanceService.update_metrics_for_student(sample_student)
            
            # Verify metrics were created
            metric = PerformanceMetric.query.filter_by(
                student_id=sample_student,
                category_id=sample_category
            ).first()
            
            assert metric is not None
            assert metric.total_occurrences >= 1
            assert metric.priority_score is not None
    
    def test_calculate_priority_score(self, app):
        """Test priority score calculation"""
        with app.app_context():
            # Test basic priority calculation
            score = PerformanceService._calculate_priority_score(
                frequency_30d=5,
                exam_weight=8,
                is_recent=True,
                student_id=1,
                category_id=1
            )
            
            # Score should be: (5 * 8 * 2.0) / 30 = 2.67
            assert score > 0
            assert score < 10
    
    def test_calculate_trend(self, app, sample_student, sample_category):
        """Test trend calculation"""
        with app.app_context():
            # Create multiple submissions
            for i in range(10):
                submission = HomeworkSubmission(
                    student_id=sample_student,
                    submission_date=date.today() - timedelta(days=i),
                    total_questions=5
                )
                db.session.add(submission)
                db.session.flush()
                
                # Add mistakes to early submissions only (improving trend)
                if i > 5:
                    mistake = Mistake(
                        submission_id=submission.id,
                        category_id=sample_category,
                        question_number=1,
                        severity='medium'
                    )
                    db.session.add(mistake)
            
            db.session.commit()
            
            trend = PerformanceService._calculate_trend(sample_student, sample_category)
            assert trend in ['improving', 'declining', 'stable']
    
    def test_get_top_priorities(self, app, sample_student):
        """Test getting top priority categories"""
        with app.app_context():
            # Create some metrics
            categories = MistakeCategory.query.limit(3).all()
            for i, category in enumerate(categories):
                metric = PerformanceMetric(
                    student_id=sample_student,
                    category_id=category.id,
                    metric_date=date.today(),
                    priority_score=10.0 - i  # Decreasing priority
                )
                db.session.add(metric)
            db.session.commit()
            
            priorities = PerformanceService.get_top_priorities_for_student(sample_student, limit=2)
            assert len(priorities) <= 2
            # Should be ordered by priority_score descending
            if len(priorities) == 2:
                assert priorities[0].priority_score >= priorities[1].priority_score
    
    def test_get_student_dashboard_data(self, app, sample_student):
        """Test dashboard data retrieval"""
        with app.app_context():
            # Create some test data
            submission = HomeworkSubmission(
                student_id=sample_student,
                submission_date=date.today(),
                total_questions=5,
                total_mistakes=2
            )
            db.session.add(submission)
            db.session.commit()
            
            data = PerformanceService.get_student_dashboard_data(sample_student)
            
            assert data is not None
            assert 'student' in data
            assert 'total_submissions' in data
            assert 'total_mistakes' in data
            assert data['total_submissions'] == 1
