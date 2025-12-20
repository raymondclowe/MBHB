# Test Fixtures

This directory contains sample data files used for testing the MBHB system.

## Files

### Homework Submissions

- `sample_homework_submission.json` - Standard test homework with various mistake types
- `homework_perfect_score.json` - Homework with no mistakes (perfect submission)
- `homework_algebra_errors.json` - Focused on algebra mistakes
- `homework_calculus_errors.json` - Focused on calculus mistakes
- `homework_empty.json` - Edge case: empty submission
- `homework_malformed.json` - Edge case: invalid structure for error handling

### Generated Worksheets

- `sample_generated_worksheet.html` - Sample worksheet for validation testing

## Usage

These fixtures are used by:
- Unit tests in `tests/test_*.py`
- Integration tests in `tests/integration/`
- CI/CD workflows in `.github/workflows/`

## Important Notes

1. **No Real Data**: All data in these fixtures is synthetic/fake
2. **Student IDs**: Use TEST* prefix (e.g., TEST001, TEST002)
3. **Dates**: Use dates from 2024 onwards
4. **Content**: Safe, appropriate educational content only

## Creating New Fixtures

When adding new test fixtures:

1. Use the same JSON schema as production data
2. Include diverse mistake types for comprehensive testing
3. Add edge cases that might break the system
4. Document the purpose of each fixture
5. Keep files small (<100 KB)

## Example Structure

```json
{
  "student_id": "TEST001",
  "student_name": "Test Student Name",
  "homework_date": "2024-01-15",
  "questions": [
    {
      "question_number": 1,
      "topic": "Topic Name",
      "student_answer": "...",
      "correct_answer": "...",
      "mistakes": [...]
    }
  ]
}
```
