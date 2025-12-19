"""Pytest configuration and fixtures"""

import pytest
import os
import tempfile
from app import create_app, db
from app.models import Student, MistakeCategory, HomeworkSubmission, Mistake


@pytest.fixture(scope='function')
def app():
    """Create and configure a test Flask application instance"""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'LOGIN_DISABLED': True  # Disable Flask-Login for testing
    })
    
    # Add a dummy user_loader to satisfy Flask-Login
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return None
    
    # Create the database and tables
    with app.app_context():
        db.create_all()
        
        # Initialize default categories
        from app.utils.init_categories import initialize_default_categories
        initialize_default_categories()
    
    yield app
    
    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_student(app):
    """Create a sample student for testing"""
    with app.app_context():
        student = Student(
            student_id='TEST001',
            name='Test Student',
            email='test@example.com',
            grade_level='IB HL Year 2'
        )
        db.session.add(student)
        db.session.commit()
        return student.id


@pytest.fixture
def sample_category(app):
    """Get a sample category for testing"""
    with app.app_context():
        category = MistakeCategory.query.filter_by(category_id='CAT001').first()
        return category.id


@pytest.fixture
def sample_homework_data():
    """Sample homework JSON data"""
    return {
        "student_id": "TEST001",
        "student_name": "Test Student",
        "homework_date": "2024-01-15",
        "questions": [
            {
                "question_number": 1,
                "topic": "Algebra",
                "student_answer": "x = 5",
                "correct_answer": "x = ±5",
                "mistakes": [
                    {
                        "type": "missing_negative_root",
                        "description": "Student forgot negative solution",
                        "severity": "high"
                    }
                ]
            },
            {
                "question_number": 2,
                "topic": "Calculus",
                "student_answer": "∫2x dx = x²",
                "correct_answer": "∫2x dx = x² + C",
                "mistakes": [
                    {
                        "type": "missing_integration_constant",
                        "description": "Forgot constant of integration",
                        "severity": "medium"
                    }
                ]
            }
        ]
    }
