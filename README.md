# Math Breakthrough Builder (MBHB)

A comprehensive AI-powered system for student performance analysis and adaptive worksheet generation. Math Breakthrough Builder automatically monitors student homework, analyzes areas for improvement, tracks performance patterns, and generates targeted practice worksheets to help students achieve breakthrough improvements in mathematics.

## 🎯 System Overview

Math Breakthrough Builder (MBHB) consists of two integrated components:

### 1. **Flask Web Application** (NEW)
- **Admin Panel**: Web-based interface for managing students and viewing analytics
- **File Monitoring**: Automatically processes submitted homework
- **Analysis Engine**: Categorizes mistakes and tracks performance
- **Performance Metrics**: Calculates trends, priorities, and improvement rates
- **Automated Worksheet Generation**: Creates targeted practice based on student needs

### 2. **Worksheet Generator** (Original)
- AI-powered HTML/JavaScript worksheet creation
- Progressive difficulty with strategic blanks
- Dynamic calculations with eval()
- Trick questions for conceptual testing
- Self-contained, printable worksheets

## ✨ Key Features

### Performance Analysis System
- **Automated Homework Monitoring**: Watches folder for new submissions
- **AI Analysis Integration**: Processes AI-analyzed homework (JSON format)
- **Pattern Identification**: 15+ pre-configured IB HL AA Math improvement areas
- **Trend Analysis**: Tracks improving, declining, or stable performance
- **Priority Scoring**: Calculates worksheet priorities based on frequency × exam weight × recency

### Student Tracking
- **Individual Profiles**: Complete performance history per student
- **Performance Metrics**: Recent vs. historical patterns
- **Progress Monitoring**: Track improvement after targeted practice
- **Dashboard Views**: Visual analytics and trends

### Worksheet Generation
- **AI-Generated Content**: Uses Gemini 2.0 Flash via OpenRouter
- **Priority-Based**: Automatically targets highest-priority improvement areas
- **Progressive Difficulty**: Questions progress from partial to complete solutions
- **Conceptual Testing**: Includes varied problem types
- **Dynamic Calculations**: JavaScript with eval() for numerical accuracy
- **Exam-Optimized**: Prioritized by IB HL AA Mathematics point values

## 🚀 Quick Start

### Option 1: Full System (Flask + Worksheet Generator)

1. **Clone and Install**:
```bash
git clone https://github.com/raymondclowe/MBHB.git
cd MBHB

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

2. **Configure**:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```
Get your API key from [OpenRouter](https://openrouter.ai/keys)

3. **Run**:
```bash
# Terminal 1: Start Flask web app
python run.py

# Terminal 2: Start file monitor
python monitor.py
```

4. **Access**: Open http://localhost:5000

### Option 2: Worksheet Generator Only (Original)

```bash
npm install
export OPENROUTER_API_KEY="your-key"
npm run cli  # Interactive mode
```

See [FLASK_SETUP.md](FLASK_SETUP.md) for detailed Flask setup instructions

## Usage

### Interactive CLI

Run the interactive command-line interface:

```bash
node cli.js
```

This will:
1. Show you a list of example bad habits
2. Let you select one or create a custom one
3. Generate a worksheet HTML file in the `output/` directory

### Programmatic Usage

```javascript
const { generateWorksheet, saveWorksheet } = require('./index');

const badHabit = "Forgetting to distribute the negative sign when expanding -(a + b)";
const example1 = "Simplify: -(3 + x). Correct: -3 - x. Common mistake: -3 + x";
const example2 = "Simplify: -(5 - 2y). Correct: -5 + 2y. Common mistake: -5 - 2y";
const newProblem = "Expanding expressions with negative signs in front of parentheses";

const apiKey = process.env.OPENROUTER_API_KEY;

generateWorksheet(badHabit, example1, example2, newProblem, apiKey)
  .then(html => {
    saveWorksheet(html, './output/my-worksheet.html');
  });
```

### Direct Execution

Run with the default example:

```bash
npm start
```

## Example Bad Habits

The system comes with several pre-configured examples:

1. **Negative Sign Distribution** - Forgetting to distribute negative signs
2. **Order of Operations** - Ignoring PEMDAS/BODMAS rules
3. **Fraction Addition** - Adding numerators and denominators incorrectly
4. **Squaring Binomials** - Forgetting the middle term (2ab)
5. **Canceling Terms** - Incorrectly canceling across addition

See `examples.js` for the complete list.

## How It Works

1. **Input**: Provide a bad habit description, two worked examples, and a problem description
2. **AI Generation**: The system sends a carefully crafted prompt to Gemini via OpenRouter
3. **HTML Creation**: AI generates a complete HTML file with embedded JavaScript
4. **Dynamic Calculations**: JavaScript uses eval() to compute correct answers dynamically
5. **Output**: A printable HTML worksheet with progressive difficulty and answer sheets

## Generated Worksheet Structure

Each worksheet includes:

- **Header**: Title and description of the bad habit
- **Worked Examples**: Two examples with the key mistake field blanked out
- **Practice Questions** (10 total):
  - Questions 1-3: Only key fields blank
  - Questions 4-7: Multiple intermediate steps blank
  - Questions 8-10: Complete solutions required
- **Trick Questions** (3 total): Interspersed questions that don't require the correction
- **Answer Sheet**: Hidden by default, accessible via button

## Requirements

- Node.js 12 or higher
- OpenRouter API key
- Internet connection for API calls

## Security Note

Generated worksheets use `eval()` or `Function` constructor to dynamically calculate mathematical answers. This is safe because:
- The calculations are generated by the AI and embedded in the HTML at generation time
- No user input is ever passed to eval()
- The worksheets are static HTML files for offline use
- Users should review generated worksheets before distribution, as with any AI-generated content

## Configuration

Copy `.env.example` to `.env` and add your API key:

```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

## Output

Generated worksheets are saved in the `output/` directory with timestamps:
- `worksheet-2024-01-15T10-30-45.html`

Open in any web browser to view, complete, or print.

## License

ISC

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
