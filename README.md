# MBHB - Math Bad Habit Breaker

An AI-powered worksheet generator that creates targeted practice materials to help students break specific math bad habits through progressive practice.

## Overview

MBHB uses AI (via OpenRouter and Gemini) to generate interactive HTML worksheets that:
- Focus on a specific math bad habit
- Provide worked examples with strategic blanks
- Generate progressive practice questions (from partial blanks to complete solutions)
- Include "trick" questions that test understanding
- Calculate correct answers using JavaScript eval() for numerical accuracy
- Provide a separate answer sheet for verification

## Features

- **AI-Generated Content**: Uses Gemini 3 Pro via OpenRouter to create custom worksheets
- **Progressive Difficulty**: Questions start with minimal blanks and progress to complete solutions
- **Trick Questions**: Interspersed questions that are similar but don't require the bad habit correction
- **Dynamic Calculations**: JavaScript generates and validates all numeric values
- **Printable Format**: Professional, printer-friendly HTML with proper formatting
- **Answer Sheets**: Hidden answer sheets that can be revealed or printed separately

## Installation

1. Clone the repository:
```bash
git clone https://github.com/raymondclowe/MBHB.git
cd MBHB
```

2. Install dependencies:
```bash
npm install
```

3. Set up your OpenRouter API key:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Get your API key from [OpenRouter](https://openrouter.ai/keys)

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
