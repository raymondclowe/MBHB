# Homework Submissions

This directory is monitored by the MBHB file monitor service. Drop AI-analyzed homework files here for automatic processing.

## Supported Formats

- **JSON files** (`.json`) - AI-analyzed homework in JSON format (currently supported)
- **Image files** (`.jpg`, `.png`) - Scanned handwritten work (OCR coming soon)
- **PDF files** (`.pdf`) - Scanned homework documents (OCR coming soon)

## JSON Format Example

```json
{
  "student_id": "12345",
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
    }
  ]
}
```
