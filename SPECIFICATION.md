# MBHB Student Performance Analysis System - Technical Specification

## Executive Summary

This specification defines a comprehensive student performance tracking and adaptive worksheet generation system that integrates with the existing Math Bad Habit Breaker (MBHB) worksheet generator. The system monitors student homework, analyzes mistakes using AI, tracks performance patterns, prioritizes learning objectives based on IB HL AA Mathematics exam scoring, and automatically generates targeted practice worksheets.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Web Application                        │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ Admin Panel  │  │  API Server  │  │ Worksheet Manager  │    │
│  └──────────────┘  └──────────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Analysis Engine (Python)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ File Monitor │  │ AI Analyzer  │  │ Category Manager   │    │
│  └──────────────┘  └──────────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database (SQLite)                           │
│  • Students    • Mistake Categories    • Performance Metrics    │
│  • Homework    • AI Analysis Results   • Generated Worksheets   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               Node.js Worksheet Generator (Existing)             │
│                    OpenRouter + Gemini                           │
└─────────────────────────────────────────────────────────────────┘
```

## 1. Core Components

### 1.1 Flask Web Application

**Purpose**: Provide administrative interface for managing students, reviewing analysis, and generating worksheets

**Key Features**:
- Student management (add, edit, view profiles)
- Dashboard showing student performance metrics
- Mistake category browsing and editing
- Manual worksheet generation trigger
- System configuration and settings
- Progress visualization (charts and graphs)

**Technologies**:
- Flask 3.0+
- SQLAlchemy for ORM
- Flask-Login for authentication
- Bootstrap 5 for UI
- Chart.js for visualizations

### 1.2 File Monitoring System

**Purpose**: Continuously monitor a designated folder for new student homework submissions

**Behavior**:
- Watch specified directory for new files (`.jpg`, `.png`, `.pdf`, `.json`)
- Trigger analysis pipeline when new files detected
- Support multiple file formats:
  - Images (scanned handwritten work)
  - PDFs (scanned homework)
  - JSON (pre-analyzed AI output from external systems)

**Implementation**: Python `watchdog` library

### 1.3 AI Analysis Engine

**Purpose**: Process student homework and extract mistake information

**Input Types**:

1. **JSON Format** (from external AI systems):
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
          "description": "Student forgot negative solution when solving x² = 25",
          "severity": "high"
        }
      ]
    }
  ]
}
```

2. **Image/PDF Format**: Future enhancement using OCR + Vision AI

**Output**: Normalized mistake records stored in database

### 1.4 Mistake Categorization System

**Purpose**: Organize mistakes into meaningful categories and track patterns

**Pre-defined Categories** (IB HL AA Math Common Mistakes):

| Category ID | Category Name | Description | Exam Weight |
|------------|---------------|-------------|-------------|
| CAT001 | Missing Negative Roots | Forgetting ±√ solutions | High (8/10) |
| CAT002 | Sign Change Error | Not changing sign when moving terms | High (9/10) |
| CAT003 | Unit Omission | Missing units in final answer | Medium (5/10) |
| CAT004 | Rounding Error | Incorrect decimal places | Medium (4/10) |
| CAT005 | Domain Restriction | Forgetting to state domain/range | High (7/10) |
| CAT006 | Integration Constant | Missing +C in indefinite integrals | High (8/10) |
| CAT007 | Chain Rule Error | Incorrect derivative application | High (9/10) |
| CAT008 | Trigonometric Identity | Wrong trig identity or simplification | Medium (6/10) |
| CAT009 | Matrix Operation | Incorrect matrix multiplication | Medium (6/10) |
| CAT010 | Probability Notation | Missing P() or incorrect notation | Low (3/10) |

**Dynamic Categories**:
- System can create new categories when mistakes don't fit existing ones
- Admin can merge, split, or rename categories
- Categories have:
  - Unique ID
  - Name and description
  - Exam weight (priority score 1-10)
  - Example mistakes
  - Related topic tags

### 1.5 Performance Tracking System

**Metrics Tracked**:

1. **Frequency Metrics**:
   - Total occurrences of each mistake type
   - Occurrences per time period (last 7 days, 30 days, all time)
   - Mistake rate (mistakes per assignment)

2. **Recency Metrics**:
   - Moving average (last 10 assignments)
   - Trend direction (improving/declining/stable)
   - Days since last occurrence

3. **Priority Score**:
   ```
   Priority Score = (Frequency × Exam Weight × Recency Factor) / Time Since Last Worksheet
   
   Where:
   - Frequency = mistakes in last 30 days
   - Exam Weight = 1-10 (from category definition)
   - Recency Factor = 2.0 if occurred in last 7 days, else 1.0
   - Time Since Last Worksheet = days since targeted practice (max 30)
   ```

4. **Improvement Tracking**:
   - Baseline error rate (before intervention)
   - Current error rate (after worksheet practice)
   - Improvement percentage
   - Statistical significance of improvement

### 1.6 Worksheet Generator Integration

**Purpose**: Automatically generate targeted practice worksheets using existing Node.js system

**Process**:
1. Python backend calculates priority scores for all mistake categories
2. Selects top-priority mistake for student
3. Calls Node.js worksheet generator via subprocess or HTTP API
4. Stores generated worksheet metadata in database
5. Tracks when worksheet was assigned and completed

**Worksheet Tracking**:
- Date generated
- Mistake category targeted
- Student ID
- Completion status
- Post-worksheet performance metrics

## 2. Database Schema

### 2.1 Students Table
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    grade_level VARCHAR(20),
    exam_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.2 Mistake Categories Table
```sql
CREATE TABLE mistake_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    exam_weight INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 Homework Submissions Table
```sql
CREATE TABLE homework_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    submission_date DATE NOT NULL,
    file_path VARCHAR(255),
    analysis_status VARCHAR(20) DEFAULT 'pending',
    total_questions INTEGER,
    total_mistakes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

### 2.4 Mistakes Table
```sql
CREATE TABLE mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    question_number INTEGER,
    description TEXT,
    severity VARCHAR(20),
    student_answer TEXT,
    correct_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submission_id) REFERENCES homework_submissions(id),
    FOREIGN KEY (category_id) REFERENCES mistake_categories(id)
);
```

### 2.5 Performance Metrics Table
```sql
CREATE TABLE performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    metric_date DATE NOT NULL,
    total_occurrences INTEGER DEFAULT 0,
    recent_occurrences_7d INTEGER DEFAULT 0,
    recent_occurrences_30d INTEGER DEFAULT 0,
    moving_average REAL,
    trend VARCHAR(20),
    priority_score REAL,
    last_occurrence_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (category_id) REFERENCES mistake_categories(id)
);
```

### 2.6 Generated Worksheets Table
```sql
CREATE TABLE generated_worksheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_at TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'generated',
    pre_worksheet_error_rate REAL,
    post_worksheet_error_rate REAL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (category_id) REFERENCES mistake_categories(id)
);
```

## 3. API Endpoints

### 3.1 Student Management

- `GET /api/students` - List all students
- `GET /api/students/<id>` - Get student details
- `POST /api/students` - Create new student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

### 3.2 Analysis

- `GET /api/students/<id>/performance` - Get performance metrics
- `GET /api/students/<id>/mistakes` - Get mistake history
- `GET /api/categories` - List mistake categories
- `POST /api/analyze` - Trigger manual analysis

### 3.3 Worksheets

- `GET /api/worksheets` - List generated worksheets
- `GET /api/students/<id>/worksheets` - Get student's worksheets
- `POST /api/worksheets/generate` - Generate new worksheet
- `PUT /api/worksheets/<id>/complete` - Mark worksheet as completed

### 3.4 Dashboard

- `GET /api/dashboard/summary` - Overall system metrics
- `GET /api/students/<id>/dashboard` - Student dashboard data

## 4. Admin Panel UI

### 4.1 Dashboard (Home Page)

**Components**:
- Active students count
- Total mistakes analyzed this week
- Worksheets generated/completed ratio
- System status indicators

**Charts**:
- Mistake trends over time (line chart)
- Top 5 mistake categories (bar chart)
- Student progress heatmap

### 4.2 Students Page

**Features**:
- Searchable/sortable student list
- Quick stats per student (total mistakes, improvement %)
- "View Details" button → Student Profile Page

### 4.3 Student Profile Page

**Sections**:
1. **Student Info**: Name, ID, exam date
2. **Performance Overview**: Overall statistics
3. **Mistake Categories Table**:
   - Category name
   - Total occurrences
   - Recent (7d) occurrences
   - Trend (↑↓→)
   - Priority score
   - Last worksheet date
   - Action button ("Generate Worksheet")
4. **Recent Homework**: List of recent submissions
5. **Worksheet History**: Generated worksheets and status

### 4.4 Categories Page

**Features**:
- List of all mistake categories
- Edit category properties (name, description, exam weight)
- Merge categories
- Create new categories
- Deactivate categories

### 4.5 Analysis Queue Page

**Features**:
- List of pending homework files
- Analysis status (pending/processing/complete/failed)
- Manual trigger for stuck analyses
- Error logs for failed analyses

### 4.6 Settings Page

**Configuration Options**:
- Homework folder path
- File monitoring interval
- OpenRouter API key
- Worksheet generation settings
- Email notifications
- Backup/export data

## 5. Implementation Phases

### Phase 1: Core Infrastructure (Days 1-2)
- Set up Flask application structure
- Create database models with SQLAlchemy
- Implement basic CRUD for students and categories
- Create admin authentication

### Phase 2: File Monitoring & Analysis (Days 3-4)
- Implement file watcher using watchdog
- Build JSON parser for AI-analyzed homework
- Create mistake categorization logic
- Implement performance metrics calculation

### Phase 3: Admin Panel UI (Days 5-6)
- Build dashboard with Bootstrap
- Create student management pages
- Implement performance visualization with Chart.js
- Build category management interface

### Phase 4: Worksheet Integration (Day 7)
- Create Python-to-Node.js bridge
- Implement priority-based worksheet generation
- Build worksheet tracking system
- Add automated worksheet scheduling

### Phase 5: Advanced Features (Day 8)
- Implement trend analysis
- Add improvement tracking
- Create reporting system
- Build data export functionality

### Phase 6: Testing & Documentation (Days 9-10)
- Write unit tests for analysis engine
- Integration tests for full pipeline
- Performance testing
- Complete user documentation
- API documentation

## 6. Configuration File

`config.yaml`:
```yaml
app:
  secret_key: "random-secret-key"
  debug: false
  host: "0.0.0.0"
  port: 5000

database:
  uri: "sqlite:///mbhb.db"

homework_monitor:
  watch_folder: "./homework_submissions"
  check_interval: 10  # seconds
  supported_formats: [".json", ".jpg", ".png", ".pdf"]

worksheet_generator:
  node_executable: "node"
  generator_script: "./index.js"
  output_folder: "./generated_worksheets"
  openrouter_api_key: "${OPENROUTER_API_KEY}"

analysis:
  default_exam_weight: 5
  priority_threshold: 10.0
  min_occurrences_for_worksheet: 2
  moving_average_window: 10

categories:
  auto_create: true
  similarity_threshold: 0.8
```

## 7. Success Metrics

1. **System Performance**:
   - Analysis latency < 5 seconds per homework
   - Dashboard load time < 2 seconds
   - Worksheet generation < 30 seconds

2. **Educational Effectiveness**:
   - Average mistake reduction: 40% after 3 targeted worksheets
   - Student engagement: 80% worksheet completion rate
   - Improvement sustainability: 70% maintain improvement after 30 days

3. **Operational Metrics**:
   - System uptime: 99%+
   - Analysis accuracy: 95%+ correct categorization
   - False positive rate: < 5%

## 8. Security Considerations

1. **Authentication**: Admin panel requires login
2. **Data Privacy**: Student data encrypted at rest
3. **API Security**: Rate limiting, input validation
4. **File Security**: Sanitize uploaded files, virus scanning
5. **Backup**: Daily automated backups

## 9. Future Enhancements

1. **OCR Integration**: Automatic handwriting recognition
2. **Multi-language Support**: Non-English exams
3. **Parent Portal**: View student progress
4. **Mobile App**: Native iOS/Android apps
5. **AI Tutor**: Chatbot for explaining mistakes
6. **Collaborative Features**: Teacher annotations
7. **Advanced Analytics**: Predictive modeling
8. **Gamification**: Achievement badges, progress rewards

## 10. Technology Stack Summary

**Backend**:
- Python 3.9+
- Flask 3.0
- SQLAlchemy 2.0
- watchdog 3.0

**Frontend**:
- Bootstrap 5
- Chart.js 4.0
- jQuery 3.7

**Database**:
- SQLite 3 (dev/small deployments)
- PostgreSQL (production recommendation)

**Integration**:
- Node.js (existing worksheet generator)
- OpenRouter API
- Gemini 2.0 Flash

**Development Tools**:
- pytest (testing)
- black (code formatting)
- flake8 (linting)
- SQLite Browser (database management)

---

**Document Version**: 1.0  
**Date**: 2024-01-19  
**Status**: Ready for Implementation
