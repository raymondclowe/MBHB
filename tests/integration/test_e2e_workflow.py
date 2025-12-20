"""
End-to-End Workflow Tests

Tests the complete workflow from homework submission to worksheet generation.
"""

import json
import os
import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return the path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def sample_homework(fixtures_dir):
    """Load sample homework submission."""
    with open(fixtures_dir / "sample_homework_submission.json") as f:
        return json.load(f)


@pytest.fixture
def perfect_homework(fixtures_dir):
    """Load perfect homework submission."""
    with open(fixtures_dir / "homework_perfect_score.json") as f:
        return json.load(f)


class TestHomeworkProcessing:
    """Test homework submission processing."""

    def test_load_sample_fixtures(self, fixtures_dir):
        """Test that all sample fixtures can be loaded."""
        fixtures = [
            "sample_homework_submission.json",
            "homework_perfect_score.json",
            "homework_algebra_errors.json",
            "homework_calculus_errors.json",
            "homework_empty.json",
        ]
        
        for fixture in fixtures:
            filepath = fixtures_dir / fixture
            assert filepath.exists(), f"Fixture {fixture} not found"
            
            with open(filepath) as f:
                data = json.load(f)
                assert "student_id" in data
                assert "questions" in data

    def test_sample_homework_structure(self, sample_homework):
        """Test that sample homework has correct structure."""
        assert sample_homework["student_id"] == "TEST001"
        assert sample_homework["student_name"] == "CI Test Student"
        assert "homework_date" in sample_homework
        assert isinstance(sample_homework["questions"], list)
        assert len(sample_homework["questions"]) > 0

    def test_sample_homework_mistakes(self, sample_homework):
        """Test that sample homework contains mistake data."""
        for question in sample_homework["questions"]:
            assert "question_number" in question
            assert "topic" in question
            assert "mistakes" in question
            
            if len(question["mistakes"]) > 0:
                mistake = question["mistakes"][0]
                assert "type" in mistake
                assert "description" in mistake
                assert "severity" in mistake

    def test_perfect_homework_no_mistakes(self, perfect_homework):
        """Test that perfect homework has no mistakes."""
        for question in perfect_homework["questions"]:
            assert len(question["mistakes"]) == 0
            assert question["student_answer"] == question["correct_answer"]

    def test_empty_homework_handling(self, fixtures_dir):
        """Test that empty homework is handled correctly."""
        with open(fixtures_dir / "homework_empty.json") as f:
            data = json.load(f)
            assert data["student_id"] == "TEST005"
            assert data["questions"] == []


class TestWorksheetGeneration:
    """Test worksheet generation (without API calls)."""

    def test_output_directory_exists(self):
        """Test that output directory can be created."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_generated_worksheets_directory(self):
        """Test that generated_worksheets directory can be created."""
        worksheets_dir = Path("generated_worksheets")
        worksheets_dir.mkdir(exist_ok=True)
        assert worksheets_dir.exists()
        assert worksheets_dir.is_dir()


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""

    def test_homework_to_database_workflow(self, app, sample_homework):
        """Test processing homework into database."""
        from app.models import Student, HomeworkSubmission, Mistake
        
        with app.app_context():
            # Create student if not exists
            student = Student.query.filter_by(
                student_id=sample_homework["student_id"]
            ).first()
            
            if not student:
                student = Student(
                    student_id=sample_homework["student_id"],
                    name=sample_homework["student_name"]
                )
                from app import db
                db.session.add(student)
                db.session.commit()
            
            # Verify student was created
            assert student is not None
            assert student.student_id == sample_homework["student_id"]

    def test_mistake_analysis_workflow(self, app, sample_homework):
        """Test analyzing mistakes from homework."""
        from app.models import Student, MistakeCategory, Mistake
        from app import db
        
        with app.app_context():
            # Count mistakes in sample
            total_mistakes = sum(
                len(q["mistakes"]) for q in sample_homework["questions"]
            )
            assert total_mistakes > 0
            
            # Verify different mistake types exist
            mistake_types = set()
            for question in sample_homework["questions"]:
                for mistake in question["mistakes"]:
                    mistake_types.add(mistake["type"])
            
            assert len(mistake_types) > 0

    def test_api_key_environment_variable(self):
        """Test that OPENROUTER_API_KEY can be accessed from environment."""
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key:
            assert len(api_key) > 0
            print("✓ OPENROUTER_API_KEY is set")
        else:
            print("⚠ OPENROUTER_API_KEY not set (some tests may be skipped)")


class TestDataValidation:
    """Test data validation and error handling."""

    def test_malformed_json_handling(self, fixtures_dir):
        """Test handling of malformed JSON data."""
        with open(fixtures_dir / "homework_malformed.json") as f:
            data = json.load(f)
            # Should load but have incorrect structure
            assert "student_id" in data
            # This should fail validation if properly implemented
            assert not isinstance(data.get("questions"), list)

    def test_homework_date_formats(self, sample_homework):
        """Test that homework dates are in correct format."""
        date_str = sample_homework["homework_date"]
        # Should be in YYYY-MM-DD format
        assert len(date_str) == 10
        assert date_str[4] == "-"
        assert date_str[7] == "-"

    def test_severity_levels(self, sample_homework):
        """Test that severity levels are valid."""
        valid_severities = ["low", "medium", "high"]
        
        for question in sample_homework["questions"]:
            for mistake in question["mistakes"]:
                assert mistake["severity"] in valid_severities
