# MBHB Flask Application Setup Guide

## Overview

The MBHB system now includes a Python Flask web application with an admin panel for student performance analysis and automated worksheet generation.

## Architecture

```
MBHB System
├── Node.js Worksheet Generator (existing)
│   ├── index.js - OpenRouter/Gemini integration
│   ├── cli.js - Interactive CLI
│   └── examples.js - Pre-configured examples
│
└── Python Flask Application (new)
    ├── Web Admin Panel
    ├── File Monitoring Service
    ├── Analysis Engine
    ├── Performance Tracking
    └── Worksheet Management
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export OPENROUTER_API_KEY="your-api-key-here"
export SECRET_KEY="your-flask-secret-key"  # Optional, auto-generated if not set
export DATABASE_URL="sqlite:///mbhb.db"     # Optional, defaults to SQLite
```

### 3. Initialize Database

```bash
python run.py
# Database tables are created automatically on first run
```

## Running the System

### Option 1: Run Both Services Together

```bash
# Terminal 1: Start Flask web application
python run.py

# Terminal 2: Start file monitor
python monitor.py
```

### Option 2: Run Flask Only (Manual Processing)

```bash
python run.py
# Access at http://localhost:5000
```

## Usage

### 1. Access Admin Panel

Open your browser to http://localhost:5000

### 2. Add Students

- Navigate to **Students** → **Add Student**
- Enter student information
- Click **Add Student**

### 3. Submit Homework for Analysis

#### Option A: Automatic (with File Monitor running)

Drop JSON files into `homework_submissions/` folder:

```bash
cp student_homework.json homework_submissions/
# File is automatically processed
```

#### Option B: Manual via API

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_path": "./homework_submissions/test.json"}'
```

### 4. View Performance Metrics

- Navigate to **Students** → Select student
- View mistake categories, trends, and priority scores

### 5. Generate Worksheets

#### Option A: Manual via Admin Panel

- Go to student profile
- Click **Generate Worksheet** next to high-priority category

#### Option B: API

```bash
curl -X POST http://localhost:5000/api/worksheets/generate \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "category_id": 1}'
```

## JSON Homework Format

Place JSON files in `homework_submissions/` with this format:

```json
{
  "student_id": "12345",
  "student_name": "John Doe",
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
          "description": "Student forgot negative solution when solving x² = 25",
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
          "description": "Forgot to add constant of integration",
          "severity": "medium"
        }
      ]
    }
  ]
}
```

## API Endpoints

### Students

- `GET /api/students` - List all students
- `GET /api/students/<id>` - Get student details
- `GET /api/students/<id>/dashboard` - Get dashboard data
- `POST /api/students` - Create student (JSON body)

### Analysis

- `POST /api/analyze` - Trigger analysis of a file
  ```json
  {"file_path": "./homework_submissions/file.json"}
  ```

### Worksheets

- `POST /api/worksheets/generate` - Generate worksheet
  ```json
  {"student_id": 1, "category_id": 1}
  ```

### Categories

- `GET /api/categories` - List all mistake categories

## Pre-configured Mistake Categories

The system includes 15 pre-configured categories for IB HL AA Mathematics:

| ID | Category | Exam Weight (1-10) |
|----|----------|-------------------|
| CAT001 | Missing Negative Roots | 8 |
| CAT002 | Sign Change Error | 9 |
| CAT003 | Unit Omission | 5 |
| CAT004 | Rounding Error | 4 |
| CAT005 | Domain/Range Restriction | 7 |
| CAT006 | Missing Integration Constant | 8 |
| CAT007 | Chain Rule Error | 9 |
| CAT008 | Trigonometric Identity | 6 |
| CAT009 | Matrix Operation Error | 6 |
| CAT010 | Probability Notation | 3 |
| CAT011 | Negative Sign Distribution | 8 |
| CAT012 | Order of Operations | 7 |
| CAT013 | Fraction Addition | 8 |
| CAT014 | Binomial Expansion | 8 |
| CAT015 | Incorrect Cancellation | 7 |

## Performance Metrics

The system calculates:

1. **Frequency**: Total mistakes, recent (7d, 30d)
2. **Trends**: Improving, declining, or stable
3. **Priority Score**: 
   ```
   Priority = (Frequency × Exam Weight × Recency Factor) / Days Since Last Worksheet
   ```
4. **Moving Average**: Average mistakes per assignment (last 10)

## Worksheet Generation Priority

Worksheets are automatically prioritized by:
1. High frequency of mistakes (30-day window)
2. High exam weight (potential point loss)
3. Recent occurrences (within 7 days)
4. Time since last targeted practice

## Database

Default: SQLite (`mbhb.db`)

Tables:
- `students` - Student information
- `mistake_categories` - Mistake types
- `homework_submissions` - Submitted homework
- `mistakes` - Individual mistakes
- `performance_metrics` - Calculated metrics
- `generated_worksheets` - Generated worksheets

## File Structure

```
MBHB/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── student.py
│   │   ├── mistake_category.py
│   │   ├── homework_submission.py
│   │   ├── mistake.py
│   │   ├── performance_metric.py
│   │   └── generated_worksheet.py
│   ├── routes/                  # Flask routes
│   │   ├── main.py             # Dashboard
│   │   ├── students.py         # Student management
│   │   ├── analysis.py         # Analysis views
│   │   ├── worksheets.py       # Worksheet management
│   │   └── api.py              # JSON API
│   ├── services/               # Business logic
│   │   ├── analysis_service.py
│   │   ├── performance_service.py
│   │   ├── worksheet_service.py
│   │   └── file_monitor_service.py
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── ...
│   └── utils/                  # Utilities
│       └── init_categories.py
├── run.py                      # Flask app entry point
├── monitor.py                  # File monitor entry point
├── requirements.txt            # Python dependencies
└── SPECIFICATION.md            # Technical specification
```

## Development

### Run in Debug Mode

```bash
export FLASK_DEBUG=true
python run.py
```

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black app/
flake8 app/
```

## Production Deployment

For production, consider:

1. **Web Server**: Use Gunicorn or uWSGI
2. **Database**: PostgreSQL instead of SQLite
3. **Process Management**: systemd or supervisord
4. **Reverse Proxy**: Nginx or Apache
5. **HTTPS**: Let's Encrypt SSL certificate

Example production startup:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Troubleshooting

### Database Issues

```bash
# Reset database
rm mbhb.db
python run.py  # Recreates tables
```

### File Monitor Not Processing

1. Check file format matches JSON spec
2. Verify file permissions
3. Check monitor.py logs for errors

### Worksheet Generation Fails

1. Verify `OPENROUTER_API_KEY` is set
2. Check Node.js is installed
3. Verify `index.js` exports functions correctly

## Support

See also:
- [SPECIFICATION.md](SPECIFICATION.md) - Complete technical specification
- [README.md](README.md) - Main project documentation
- [USAGE.md](USAGE.md) - Original worksheet generator usage

## Next Steps

1. Add students via admin panel
2. Submit test homework files
3. Review generated performance metrics
4. Generate and review worksheets
5. Track student improvement over time
