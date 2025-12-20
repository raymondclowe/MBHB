# MBHB Testing Guide

## Overview

The MBHB project includes a comprehensive pytest test suite covering models, services, and routes.

## Test Coverage

### Test Statistics
- **Total Tests**: 35
- **Test Files**: 3
- **Code Coverage**: 75%

### Test Breakdown

#### Models Tests (`tests/test_models.py`)
- **12 tests** covering all database models
- Tests include: creation, serialization, relationships, and calculations
- Models tested: Student, MistakeCategory, HomeworkSubmission, Mistake, PerformanceMetric, GeneratedWorksheet

#### Routes Tests (`tests/test_routes.py`)
- **14 tests** covering all Flask routes
- Tests include: page rendering, form submission, API endpoints
- Routes tested: Main, Students, Analysis, Worksheets, API

#### Services Tests (`tests/test_services.py`)
- **9 tests** covering business logic
- Tests include: JSON processing, metric calculation, trend analysis
- Services tested: AnalysisService, PerformanceService

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
# Basic test run
pytest tests/

# Verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html
# View: open htmlcov/index.html
```

### Run Specific Test Files

```bash
# Models only
pytest tests/test_models.py -v

# Services only
pytest tests/test_services.py -v

# Routes only
pytest tests/test_routes.py -v
```

### Run Specific Test Classes

```bash
# Test specific model
pytest tests/test_models.py::TestStudent -v

# Test specific service
pytest tests/test_services.py::TestAnalysisService -v
```

### Run Individual Tests

```bash
# Single test
pytest tests/test_models.py::TestStudent::test_create_student -v
```

## Test Configuration

Configuration in `pytest.ini`:
- Test path: `tests/`
- Coverage: Enabled with HTML and terminal reports
- Test markers: slow, integration, unit
- Output format: Verbose with short tracebacks

## Writing New Tests

### Test Structure

```python
def test_feature_name(app, client, sample_student):
    """Clear description of what is being tested"""
    with app.app_context():
        # Arrange: Set up test data
        
        # Act: Perform the action
        
        # Assert: Verify results
        assert result == expected
```

### Available Fixtures

From `tests/conftest.py`:

- **app**: Flask application instance with test database
- **client**: Test client for making HTTP requests
- **runner**: CLI runner for testing commands
- **sample_student**: Pre-created test student (id: TEST001)
- **sample_category**: Pre-created test category (CAT001)
- **sample_homework_data**: Sample JSON homework structure

### Example: Adding a New Test

```python
# tests/test_my_feature.py

def test_my_new_feature(app, sample_student):
    """Test my new feature"""
    with app.app_context():
        # Your test code here
        student = Student.query.get(sample_student)
        assert student.name == 'Test Student'
```

## Continuous Integration

### GitHub Actions (Future)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ --cov=app
```

## Test Database

- Uses SQLite in-memory or temp file
- Fresh database for each test function
- Automatically cleaned up after test
- Pre-populated with 15 default categories

## Coverage Report

Current coverage by module:

| Module | Coverage | Lines | Missing |
|--------|----------|-------|---------|
| models/__init__.py | 100% | 7 | 0 |
| models/student.py | 95% | 19 | 1 |
| models/mistake_category.py | 95% | 19 | 1 |
| routes/main.py | 100% | 18 | 0 |
| routes/analysis.py | 100% | 11 | 0 |
| services/analysis_service.py | 94% | 64 | 4 |
| services/performance_service.py | 91% | 90 | 8 |
| **Total** | **75%** | **580** | **144** |

## Common Issues

### Database Locked
```bash
# Stop all services before running tests
sudo systemctl stop mbhb-web mbhb-monitor
pytest tests/
```

### Import Errors
```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Verify Flask app can be imported
python -c "from app import create_app; print('OK')"
```

### Fixture Not Found
```bash
# Ensure conftest.py is in tests/ directory
ls tests/conftest.py
```

## Performance Testing

### Slow Tests

Mark slow tests:
```python
@pytest.mark.slow
def test_slow_operation(app):
    # Long-running test
    pass
```

Run without slow tests:
```bash
pytest tests/ -m "not slow"
```

### Load Testing

For API load testing, use `locust`:
```bash
pip install locust
locust -f tests/locustfile.py
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Fixtures**: Use fixtures for common setup
3. **Descriptive Names**: Test names should describe what they test
4. **Fast Tests**: Keep tests fast (< 1 second each)
5. **Clean Up**: Tests should not leave artifacts
6. **Assertions**: Use specific assertions, not generic ones
7. **Coverage**: Aim for 80%+ coverage of critical paths

## Debugging Tests

### Run with pdb debugger

```bash
# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger at start
pytest tests/ --pdb -x test_specific_test
```

### Print debugging

```python
def test_with_debug(app, capsys):
    """Test with print debugging"""
    print("Debug output")
    # Test code
    captured = capsys.readouterr()
    assert "Debug output" in captured.out
```

### Verbose output

```bash
# Show all output
pytest tests/ -v -s

# Show only failed tests
pytest tests/ --tb=short
```

## Test Maintenance

### Update Fixtures

When models change, update fixtures in `conftest.py`:
```python
@pytest.fixture
def new_fixture(app):
    with app.app_context():
        # Create new test data
        pass
```

### Refactor Tests

- Extract common assertions to helper functions
- Use parametrized tests for multiple scenarios
- Keep test files under 500 lines

### Review Coverage

```bash
# Generate coverage report
pytest tests/ --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html

# Focus on untested code
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/latest/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/latest/core/testing.html)
- [Coverage.py](https://coverage.readthedocs.io/)

## Support

For test-related issues:
1. Check test output for specific error
2. Verify all fixtures are available
3. Ensure database is clean
4. Review test documentation above
