# MBHB Usage Guide

## Quick Start

### 1. Setup

First, install dependencies and set up your API key:

```bash
npm install
export OPENROUTER_API_KEY="your-api-key-here"
```

Get your API key from [OpenRouter](https://openrouter.ai/keys)

### 2. Generate Your First Worksheet

#### Option A: Use Pre-configured Examples (Interactive)

```bash
npm run cli
```

This will:
1. Show you a menu of example bad habits
2. Let you select one
3. Generate a worksheet automatically

#### Option B: Use the Default Example

```bash
npm start
```

This generates a worksheet for the default example (negative sign distribution).

#### Option C: Custom Bad Habit (Programmatic)

Create a script or modify `index.js`:

```javascript
const { generateWorksheet, saveWorksheet } = require('./index');

const badHabit = "Your bad habit description";
const example1 = "First example with correct and incorrect answer";
const example2 = "Second example with correct and incorrect answer";
const newProblem = "Problem type description";

generateWorksheet(badHabit, example1, example2, newProblem, process.env.OPENROUTER_API_KEY)
  .then(html => saveWorksheet(html, './output/custom-worksheet.html'));
```

### 3. View and Use the Worksheet

1. Open the generated HTML file in any web browser
2. Print the worksheet for students to complete
3. Click "Show Answer Sheet" to reveal answers
4. Print the answer sheet separately if needed

## Understanding the Worksheet Structure

### Bad Habit Section (Red Box)
- Explains the specific bad habit being addressed
- Shows the correct approach vs. common mistake

### Worked Examples (Blue Boxes)
- Two examples with strategic blanks
- Students must fill in the key mistake field
- Correct answers shown below for self-checking

### Practice Questions
- **Questions 1-3**: Only key fields are blank (easy)
- **Questions 4-7**: Multiple intermediate steps blank (medium)
- **Questions 8-10**: Complete solutions required (hard)
- **Trick Questions** (marked with *): Similar problems that DON'T require the bad habit correction

### Answer Sheet
- Hidden by default
- Accessible via "Show Answer Sheet" button
- Contains complete solutions with step-by-step explanations
- Can be printed separately

## Available Examples

The system comes with 5 pre-configured examples:

1. **Negative Sign Distribution** - Forgetting to distribute negative signs
2. **Order of Operations** - Ignoring PEMDAS/BODMAS rules
3. **Fraction Addition** - Adding numerators and denominators incorrectly
4. **Squaring Binomials** - Forgetting the middle term (2ab)
5. **Canceling Terms** - Incorrectly canceling across addition

See `examples.js` for the complete configuration of each example.

## Creating Custom Bad Habits

To create your own bad habit worksheet, you need to provide:

### 1. Bad Habit Description
A clear statement of the specific mistake students make.

**Example:**
```
"Forgetting to distribute the negative sign when expanding -(a + b)"
```

### 2. First Example
A worked example showing the problem, correct answer, and common mistake.

**Format:**
```
"Problem statement. Correct: [correct answer]. Common mistake: [wrong answer]"
```

**Example:**
```
"Simplify: -(3 + x). Correct: -3 - x. Common mistake: -3 + x"
```

### 3. Second Example
Another worked example in the same format, preferably with a slightly different structure.

**Example:**
```
"Simplify: -(5 - 2y). Correct: -5 + 2y. Common mistake: -5 - 2y"
```

### 4. Problem Description
A general description of the problem type for the AI to generate variations.

**Example:**
```
"Expanding expressions with negative signs in front of parentheses"
```

## Tips for Best Results

### For Educators

1. **Choose Specific Bad Habits**: The more specific the bad habit, the better the worksheet
2. **Review Generated Content**: Always review the AI-generated worksheet before using with students
3. **Customize Examples**: Provide examples that match your curriculum level
4. **Print Quality**: Use landscape orientation for better readability

### For Students

1. **Start with Examples**: Carefully study the worked examples first
2. **Watch for Tricks**: Questions marked with * might not need the correction
3. **Show Your Work**: Use the blank space to write out all steps
4. **Self-Check**: Use the answer sheet to verify your solutions

### For Developers

1. **Error Handling**: The system will display clear error messages if API key is missing
2. **Output Location**: All worksheets are saved in the `output/` directory
3. **HTML Structure**: Generated worksheets are self-contained (no external dependencies)
4. **Customization**: Modify `sample-worksheet.html` to see the expected output format

## Troubleshooting

### "OPENROUTER_API_KEY environment variable not set"
- Solution: Export your API key: `export OPENROUTER_API_KEY="your-key"`
- Verify: `echo $OPENROUTER_API_KEY`

### "Error calling OpenRouter API"
- Check your API key is valid
- Verify you have internet connectivity
- Check OpenRouter service status

### "Generated worksheet doesn't open"
- Make sure you're opening the HTML file in a web browser
- Check that JavaScript is enabled in your browser
- Try a different browser (Chrome, Firefox, Safari)

### "Questions are not displaying correctly"
- Refresh the page
- Check browser console for JavaScript errors
- Verify the HTML file downloaded completely

## Advanced Usage

### Batch Generation

Generate multiple worksheets at once:

```javascript
const examples = require('./examples');
const { generateWorksheet, saveWorksheet } = require('./index');

async function generateAll() {
  for (const ex of examples) {
    const html = await generateWorksheet(
      ex.badHabit,
      ex.example1,
      ex.example2,
      ex.newProblem,
      process.env.OPENROUTER_API_KEY
    );
    saveWorksheet(html, `./output/${ex.name.replace(/\s+/g, '-')}.html`);
  }
}

generateAll();
```

### Custom Styling

The generated HTML includes inline CSS. To customize:

1. Generate a worksheet
2. Edit the `<style>` section in the generated HTML
3. Use as a template for future generations

### Integration with LMS

The generated HTML files can be:
- Uploaded to Canvas, Moodle, or other LMS
- Embedded in course websites
- Shared via Google Drive, Dropbox, etc.

## API Cost Considerations

- Uses OpenRouter API with Gemini 2.0 Flash (free tier)
- Each worksheet generation costs approximately $0 (free model)
- For heavy usage, consider upgrading to paid models for better quality
- Monitor your usage at [OpenRouter Dashboard](https://openrouter.ai/activity)

## Contributing

Found a great bad habit example? Want to improve the prompts? 

1. Fork the repository
2. Add your examples to `examples.js`
3. Test with `npm test`
4. Submit a pull request

## License

ISC - Free to use and modify
