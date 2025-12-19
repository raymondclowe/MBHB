"""Tests for Flask routes"""

import pytest
import json
from app import db
from app.models import Student


class TestMainRoutes:
    """Tests for main routes"""
    
    def test_index(self, client):
        """Test dashboard index page"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Dashboard' in response.data
    
    def test_about(self, client):
        """Test about page"""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'About MBHB' in response.data


class TestStudentRoutes:
    """Tests for student routes"""
    
    def test_list_students(self, client):
        """Test student list page"""
        response = client.get('/students/')
        assert response.status_code == 200
    
    def test_add_student_get(self, client):
        """Test add student page (GET)"""
        response = client.get('/students/add')
        assert response.status_code == 200
        assert b'Add New Student' in response.data
    
    def test_add_student_post(self, client, app):
        """Test add student (POST)"""
        response = client.post('/students/add', data={
            'student_id': 'NEW001',
            'name': 'New Student',
            'email': 'new@example.com',
            'grade_level': 'IB HL Year 2'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify student was created
        with app.app_context():
            student = Student.query.filter_by(student_id='NEW001').first()
            assert student is not None
            assert student.name == 'New Student'
    
    def test_view_student(self, client, sample_student):
        """Test view student profile"""
        response = client.get(f'/students/{sample_student}')
        assert response.status_code == 200
        assert b'Student Profile' in response.data


class TestAnalysisRoutes:
    """Tests for analysis routes"""
    
    def test_analysis_index(self, client):
        """Test analysis queue page"""
        response = client.get('/analysis/')
        assert response.status_code == 200
    
    def test_categories_page(self, client):
        """Test categories page"""
        response = client.get('/analysis/categories')
        assert response.status_code == 200


class TestWorksheetRoutes:
    """Tests for worksheet routes"""
    
    def test_list_worksheets(self, client):
        """Test worksheet list page"""
        response = client.get('/worksheets/')
        assert response.status_code == 200


class TestAPIRoutes:
    """Tests for API routes"""
    
    def test_api_list_students(self, client, app, sample_student):
        """Test API list students endpoint"""
        response = client.get('/api/students')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_api_get_student(self, client, sample_student):
        """Test API get student endpoint"""
        response = client.get(f'/api/students/{sample_student}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['student_id'] == 'TEST001'
    
    def test_api_get_student_not_found(self, client):
        """Test API get non-existent student"""
        response = client.get('/api/students/99999')
        assert response.status_code == 404
    
    def test_api_list_categories(self, client):
        """Test API list categories endpoint"""
        response = client.get('/api/categories')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 15
    
    def test_api_student_dashboard(self, client, sample_student):
        """Test API student dashboard endpoint"""
        response = client.get(f'/api/students/{sample_student}/dashboard')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'student' in data
        assert 'total_submissions' in data
    
    def test_api_generate_worksheet_missing_params(self, client):
        """Test API generate worksheet with missing parameters"""
        response = client.post('/api/worksheets/generate',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
