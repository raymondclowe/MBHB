# CI Testing Quick Reference

A concise guide for setting up continuous integration testing for MBHB.

## Essential Requirements

### 1. GitHub Secret: COPILOT_OPENROUTER_API_KEY ⭐ REQUIRED

**Get your key**: [https://openrouter.ai/keys](https://openrouter.ai/keys)

**Add to GitHub**:
1. Repository → Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `COPILOT_OPENROUTER_API_KEY`
4. Value: Your API key
5. Add secret

**Note**: The `COPILOT_` prefix is required for GitHub Actions, workflows, and Copilot sessions.

## Test Data Files (Already Created)

All test fixtures are in `tests/fixtures/`:

- ✅ `sample_homework_submission.json` - Standard test case
- ✅ `homework_perfect_score.json` - No mistakes
- ✅ `homework_algebra_errors.json` - Algebra focus
- ✅ `homework_calculus_errors.json` - Calculus focus
- ✅ `homework_empty.json` - Edge case: empty
- ✅ `homework_malformed.json` - Edge case: invalid

## Workflows (Already Created)

Three GitHub Actions workflows in `.github/workflows/`:

- ✅ `ci-python.yml` - Python/Flask tests (Python 3.9, 3.10, 3.11)
- ✅ `ci-nodejs.yml` - Node.js tests (Node 16, 18, 20)
- ✅ `ci-integration.yml` - End-to-end tests (requires API key)

## Folder Structure

```
tests/
├── fixtures/          # Test data (committed to git)
│   ├── *.json        # Sample homework files
│   └── README.md
├── integration/       # E2E tests
│   ├── __init__.py
│   └── test_e2e_workflow.py
├── conftest.py        # Pytest fixtures
├── test_models.py     # Unit tests
├── test_routes.py
└── test_services.py
```

## Running Tests Locally

```bash
# Set API key (with COPILOT_ prefix for consistency)
export COPILOT_OPENROUTER_API_KEY="your-key-here"
export OPENROUTER_API_KEY="$COPILOT_OPENROUTER_API_KEY"

# Python tests
pytest tests/ -v

# Node.js tests
npm test

# Specific test file
pytest tests/integration/test_e2e_workflow.py -v
```

## What Gets Tested

### Python Tests (ci-python.yml)
- ✓ Unit tests (models, routes, services)
- ✓ Code coverage (target: 75%+)
- ✓ Linting (flake8)
- ✓ Formatting (black)

### Node.js Tests (ci-nodejs.yml)
- ✓ Basic functionality
- ✓ Examples structure
- ✓ Required files exist

### Integration Tests (ci-integration.yml)
- ✓ End-to-end workflows
- ✓ Homework processing
- ✓ Database operations
- ✓ Worksheet generation (if API key available)
- ✓ Flask app startup

## Status Badges (Optional)

Add to README.md:

```markdown
![Python Tests](https://github.com/raymondclowe/MBHB/workflows/Python%20Tests/badge.svg)
![Node.js Tests](https://github.com/raymondclowe/MBHB/workflows/Node.js%20Tests/badge.svg)
![Integration Tests](https://github.com/raymondclowe/MBHB/workflows/Integration%20Tests/badge.svg)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "COPILOT_OPENROUTER_API_KEY not set" | Add secret in GitHub Settings with COPILOT_ prefix |
| Module not found | Check requirements.txt/package.json |
| Tests pass locally, fail in CI | Check for hardcoded paths |
| Database locked | Use separate test database |

## Next Steps

1. ✅ Add `COPILOT_OPENROUTER_API_KEY` to GitHub Secrets
2. ✅ Push code to trigger workflows
3. ✅ Check Actions tab for results
4. ✅ Fix any failures
5. ✅ Add status badges to README (optional)

## Full Documentation

See [CI_TESTING.md](CI_TESTING.md) for complete details on:
- Advanced configuration
- Multiple environments
- Security best practices
- Monitoring and maintenance
- Troubleshooting guide

## Support

- Check workflow logs: Repository → Actions tab
- Review test output for specific errors
- Verify secrets are correctly configured
- Test locally with same environment
