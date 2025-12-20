# Continuous Integration Testing Guide for MBHB

## Overview

This guide explains how to set up end-to-end continuous integration testing in GitHub Actions for the Math Breakthrough Builder (MBHB) project. It includes details on required secrets, sample data files, and how to configure everything for thorough automated testing.

## Required Secrets and API Keys

### 1. OpenRouter API Key (REQUIRED)

**Purpose**: Required for worksheet generation using AI (Gemini 2.0 Flash via OpenRouter)

**Where to get it**: 
- Visit [https://openrouter.ai/keys](https://openrouter.ai/keys)
- Create an account or sign in
- Generate a new API key

**How to add to GitHub Secrets**:
1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `COPILOT_OPENROUTER_API_KEY`
5. Value: Paste your OpenRouter API key
6. Click **Add secret**

**Usage in CI**: This will be available as `${{ secrets.COPILOT_OPENROUTER_API_KEY }}` in GitHub Actions workflows

**Note**: The `COPILOT_` prefix is required for GitHub Actions, workflows, and Copilot sessions to properly access the secret.

### 2. Flask Secret Key (OPTIONAL - Auto-generated for CI)

**Purpose**: Flask session security

**Note**: For CI testing, this is auto-generated. For production deployments, you should set a secure random value.

**How to add to GitHub Secrets** (production only):
1. Generate a secure key: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Add as secret named `FLASK_SECRET_KEY`

## Required Sample Data Files

### Location: `tests/fixtures/`

Create a `tests/fixtures/` directory to store sample test data files that will be used during CI testing.

### 1. Sample Homework Submission (JSON)

**File**: `tests/fixtures/sample_homework_submission.json`

**Purpose**: Test the homework processing and analysis pipeline

**Structure**: Based on the existing `sample_homework.json` format
```json
{
  "student_id": "TEST001",
  "student_name": "CI Test Student",
  "homework_date": "2024-01-15",
  "questions": [
    {
      "question_number": 1,
      "topic": "Algebra - Quadratic Equations",
      "student_answer": "x = 5",
      "correct_answer": "x = ±5",
      "mistakes": [
        {
          "type": "missing_negative_root",
          "description": "Student forgot negative solution",
          "severity": "high"
        }
      ]
    }
  ]
}
```

### 2. Sample Generated Worksheet (HTML)

**File**: `tests/fixtures/sample_generated_worksheet.html`

**Purpose**: Test worksheet rendering and validation without API calls

**Note**: Can use the existing `sample-worksheet.html` as a template

### 3. Test Database State

**File**: `tests/fixtures/test_database.sql` (OPTIONAL)

**Purpose**: Pre-populate test database with specific scenarios

**Note**: The existing conftest.py already handles database setup, so this is optional

## Folder Structure for CI Testing

```
MBHB/
├── .github/
│   └── workflows/
│       ├── ci-python.yml          # Python/Flask tests
│       ├── ci-nodejs.yml          # Node.js tests
│       └── ci-integration.yml     # End-to-end tests
├── tests/
│   ├── fixtures/                  # Test data files (NEW)
│   │   ├── sample_homework_submission.json
│   │   ├── sample_generated_worksheet.html
│   │   └── README.md             # Explains fixture files
│   ├── integration/              # Integration tests (NEW)
│   │   ├── __init__.py
│   │   ├── test_e2e_workflow.py
│   │   └── test_api_integration.py
│   ├── conftest.py               # Existing pytest fixtures
│   ├── test_models.py            # Existing unit tests
│   ├── test_routes.py
│   └── test_services.py
├── homework_submissions/         # Runtime folder (gitignored)
├── generated_worksheets/         # Runtime folder (gitignored)
└── output/                       # Runtime folder (gitignored)
```

## GitHub Actions Workflow Configuration

### Workflow 1: Python/Flask Tests (ci-python.yml)

```yaml
name: Python Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-python:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: |
        black --check app/ tests/
    
    - name: Run unit tests
      run: |
        pytest tests/ -v --cov=app --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
```

### Workflow 2: Node.js Tests (ci-nodejs.yml)

```yaml
name: Node.js Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-nodejs:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: ['16', '18', '20']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Verify examples structure
      run: node test.js
```

### Workflow 3: Integration Tests (ci-integration.yml)

```yaml
name: Integration Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-integration:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Install Node.js dependencies
      run: npm ci
    
    - name: Create test directories
      run: |
        mkdir -p homework_submissions
        mkdir -p generated_worksheets
        mkdir -p output
    
    - name: Set up test environment variables
      env:
        COPILOT_OPENROUTER_API_KEY: ${{ secrets.COPILOT_OPENROUTER_API_KEY }}
      run: |
        echo "OPENROUTER_API_KEY=${COPILOT_OPENROUTER_API_KEY}" >> $GITHUB_ENV
        echo "FLASK_ENV=testing" >> $GITHUB_ENV
        echo "DATABASE_URL=sqlite:///test.db" >> $GITHUB_ENV
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --maxfail=3
    
    - name: Test worksheet generation (with API)
      if: env.OPENROUTER_API_KEY != ''
      run: |
        node index.js
        ls -la output/
    
    - name: Test Flask application startup
      run: |
        timeout 10 python run.py || true
    
    - name: Upload test artifacts
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-outputs
        path: |
          output/
          generated_worksheets/
          htmlcov/
        retention-days: 7
```

## Setting Up GitHub Secrets - Step by Step

### For Repository Administrators

1. **Access Repository Settings**
   - Navigate to your repository on GitHub
   - Click on **Settings** tab (requires admin access)

2. **Navigate to Secrets**
   - In the left sidebar, expand **Secrets and variables**
   - Click on **Actions**

3. **Add OpenRouter API Key**
   - Click **New repository secret** button
   - Enter the following:
     - **Name**: `COPILOT_OPENROUTER_API_KEY`
     - **Secret**: Your actual API key from OpenRouter
   - Click **Add secret**

4. **Verify Secret is Added**
   - You should see `COPILOT_OPENROUTER_API_KEY` in the list of repository secrets
   - The actual value will be hidden (shown as `***`)

5. **Test the Secret** (Optional but Recommended)
   - Create a simple workflow that echoes a masked version
   - Example:
     ```yaml
     - name: Test secret availability
       run: |
         if [ -z "${{ secrets.COPILOT_OPENROUTER_API_KEY }}" ]; then
           echo "❌ COPILOT_OPENROUTER_API_KEY is not set"
           exit 1
         else
           echo "✅ COPILOT_OPENROUTER_API_KEY is available"
         fi
     ```

### Security Best Practices for Secrets

1. **Never commit secrets to the repository**
   - Always use GitHub Secrets
   - Keep `.env` in `.gitignore` (already configured)

2. **Use environment-specific secrets**
   - Different keys for development, staging, production
   - Use GitHub Environments for additional control

3. **Rotate secrets regularly**
   - Update API keys periodically
   - Revoke old keys after rotation

4. **Limit secret exposure**
   - Only give secrets to workflows that need them
   - Use `if` conditions to control when secrets are accessed

5. **Monitor secret usage**
   - Review workflow logs for unauthorized access attempts
   - Set up alerts for failed authentications

## Test Data Management

### What to Commit to Git

✅ **DO commit**:
- `tests/fixtures/*.json` - Sample test data with fake/anonymized information
- `tests/fixtures/*.html` - Sample worksheet templates
- `tests/fixtures/README.md` - Documentation about test fixtures

❌ **DO NOT commit**:
- Real student data
- API keys or credentials
- Generated output files (already in `.gitignore`)
- Database files (`.db`, `.sqlite`)

### Sample Test Fixtures to Create

Create these files in `tests/fixtures/`:

1. **Multiple homework scenarios**
   - `homework_perfect_score.json` - No mistakes
   - `homework_algebra_errors.json` - Algebra-focused mistakes
   - `homework_calculus_errors.json` - Calculus-focused mistakes

2. **Edge cases**
   - `homework_empty.json` - Empty submission
   - `homework_malformed.json` - Invalid structure for error handling

3. **Performance testing**
   - `homework_large_submission.json` - Many questions (50+)

## Running CI Tests Locally

### Before Pushing to GitHub

1. **Set up local environment**
   ```bash
   export COPILOT_OPENROUTER_API_KEY="your-key-here"
   export OPENROUTER_API_KEY="$COPILOT_OPENROUTER_API_KEY"
   export FLASK_ENV=testing
   ```

2. **Run Python tests**
   ```bash
   # Unit tests
   pytest tests/ -v
   
   # With coverage
   pytest tests/ --cov=app --cov-report=html
   
   # Integration tests only
   pytest tests/integration/ -v
   ```

3. **Run Node.js tests**
   ```bash
   npm test
   ```

4. **Lint checks**
   ```bash
   # Python
   flake8 app/
   black --check app/ tests/
   
   # Node.js (if configured)
   npm run lint
   ```

5. **Test worksheet generation**
   ```bash
   node index.js
   ```

### Using Act (GitHub Actions Locally)

Install [act](https://github.com/nektos/act) to run GitHub Actions on your machine:

```bash
# Install act
brew install act  # macOS
# or download from: https://github.com/nektos/act/releases

# Create secrets file
echo "COPILOT_OPENROUTER_API_KEY=your-key-here" > .secrets

# Run workflows locally
act -s COPILOT_OPENROUTER_API_KEY="$(cat .secrets)"
```

## Continuous Integration Best Practices

### 1. Fast Feedback
- Run quick tests (linting, unit tests) first
- Run slower integration tests after
- Fail fast on critical errors

### 2. Comprehensive Coverage
- Unit tests: 75%+ coverage (current goal met)
- Integration tests: All major workflows
- End-to-end tests: Critical user paths

### 3. Consistent Environments
- Use same Python/Node versions as production
- Cache dependencies to speed up builds
- Use matrix testing for multiple versions

### 4. Clear Test Organization
```
Unit Tests        → Fast, isolated, no external dependencies
Integration Tests → Moderate speed, tests component interactions
E2E Tests         → Slower, tests full user workflows
```

### 5. Artifact Preservation
- Save generated worksheets for review
- Store coverage reports
- Keep logs for debugging failures

## Monitoring and Maintenance

### Regular Tasks

**Daily**:
- Review failed CI runs
- Check for flaky tests

**Weekly**:
- Review test coverage trends
- Update dependencies if needed

**Monthly**:
- Audit secret usage
- Review and update test fixtures
- Check for deprecated actions/dependencies

### Key Metrics to Track

1. **Test Execution Time**
   - Target: < 5 minutes for full suite
   - Monitor for performance degradation

2. **Test Success Rate**
   - Target: > 95% pass rate
   - Investigate consistent failures

3. **Code Coverage**
   - Target: Maintain 75%+ coverage
   - Track coverage changes per PR

4. **Flaky Tests**
   - Target: 0 flaky tests
   - Document and fix intermittent failures

## Troubleshooting Common CI Issues

### Issue: "COPILOT_OPENROUTER_API_KEY not set"

**Solution**:
1. Verify secret is added in GitHub Settings
2. Check secret name matches exactly: `COPILOT_OPENROUTER_API_KEY`
3. Ensure workflow has access to secrets (not on fork PRs from external contributors)

### Issue: "Module not found" errors

**Solution**:
```yaml
# Add to workflow
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    npm ci
```

### Issue: Database locked errors

**Solution**:
```yaml
# Use separate test database
- name: Set up test environment
  run: |
    export DATABASE_URL=sqlite:///test_${{ github.run_id }}.db
```

### Issue: Tests pass locally but fail in CI

**Solution**:
- Check for hardcoded paths (use `os.path.join`)
- Verify all dependencies in requirements.txt/package.json
- Check for timezone-dependent tests
- Look for file system case sensitivity issues

## Advanced Configuration

### Using GitHub Environments

For production deployments with additional protection:

1. **Create Environment**
   - Settings → Environments → New environment
   - Name: `production`

2. **Add Environment Secrets**
   - Different API key for production
   - Add required reviewers

3. **Update Workflow**
   ```yaml
   jobs:
     deploy:
       environment: production
       steps:
         - uses: actions/checkout@v3
         # ... deployment steps
   ```

### Conditional Tests Based on Secret Availability

```yaml
- name: Test with API (if key available)
  if: secrets.COPILOT_OPENROUTER_API_KEY != ''
  env:
    OPENROUTER_API_KEY: ${{ secrets.COPILOT_OPENROUTER_API_KEY }}
  run: |
    node index.js

- name: Skip API tests (if no key)
  if: secrets.COPILOT_OPENROUTER_API_KEY == ''
  run: |
    echo "⚠️  Skipping API tests - COPILOT_OPENROUTER_API_KEY not available"
    echo "Tests run in offline mode"
```

### Matrix Testing for Multiple Configurations

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    os: [ubuntu-latest, macos-latest, windows-latest]
  fail-fast: false  # Continue testing other combinations if one fails
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Pytest Documentation](https://docs.pytest.org/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)

## Support

For issues with CI setup:
1. Check workflow logs in GitHub Actions tab
2. Review this documentation
3. Verify all secrets are correctly configured
4. Test locally with same environment
5. Open an issue with workflow logs attached
