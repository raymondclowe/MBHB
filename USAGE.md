# MBHB Usage Guide

## Quick Start

1. **Open the Generator**
   - Double-click `index.html` or open it in any web browser
   - No installation required!

2. **Fill in the Form**
   - The form comes pre-filled with an example about negative sign distribution
   - You can use this example or replace it with your own

3. **Generate Your Worksheet**
   - Click the "Generate Worksheet" button
   - Your custom worksheet appears instantly

4. **Print or Save**
   - Click the "🖨️ Print Worksheet" button
   - Or use your browser's print function (Ctrl+P / Cmd+P)
   - Save as PDF for digital distribution

## Form Fields Explained

### Required Fields

- **Bad Habit Description**: Describe the mistake students commonly make
  - Example: "Students forget to distribute the negative sign"

- **Example 1 - Problem**: First practice problem
  - Example: "Simplify: -(3x + 5)"

- **Example 1 - Complete Answer**: The correct full answer
  - Example: "-3x - 5"

- **New Practice Problem**: A fresh problem for students
  - Example: "Simplify: -(4a + 9)"

### Optional Fields

- **AI Template Prompt**: Explain the correct approach
  - This appears in the "Understanding the Pattern" section
  - Helps students understand WHY the bad habit is wrong

- **Example 2**: Add a second example for more practice
  - Same structure as Example 1

- **Key Mistake Fields**: Specify what to blank out
  - The part of the answer students often get wrong
  - This creates the blank line for hand-writing practice
  - If left empty, the entire answer becomes a blank line

- **Complete Answer (for practice problem)**: Your reference answer
  - If provided: creates a partially-filled answer with blank
  - If omitted: creates a completely blank answer line

## Creating Effective Worksheets

### Tips for Bad Habit Descriptions

✅ **Good**: "Students often add fractions by adding both numerators AND denominators"
❌ **Too vague**: "Students make mistakes with fractions"

### Tips for Key Mistake Fields

- Enter the EXACT text that should be blanked out
- Include spacing to match the answer exactly
- Example: If answer is "-3x - 5", enter "- 5" to blank the second term

### Tips for AI Template Prompts

- Explain the correct method step-by-step
- Use concrete examples
- Emphasize the key point students miss
- Keep it concise but clear

## Example Use Cases

### 1. Algebra - Distribution
**Bad Habit**: Forgetting to distribute negative signs
**Worksheet Focus**: Practice with -(a+b) expressions

### 2. Fractions - Addition
**Bad Habit**: Adding numerators and denominators
**Worksheet Focus**: Finding common denominators first

### 3. Order of Operations
**Bad Habit**: Working left-to-right without following PEMDAS
**Worksheet Focus**: Identifying which operation to do first

### 4. Exponents - Multiplication
**Bad Habit**: Adding exponents when multiplying different bases
**Worksheet Focus**: When to add vs. multiply exponents

## Advanced Features

### Multiple Blank Spaces

If a key mistake field appears multiple times in the answer, ALL occurrences will be blanked out. This is useful for patterns that repeat.

Example:
- Answer: "2x + 3y + 2x + 3y"
- Key Mistake Field: "+ 3y"
- Result: "2x _____ + 2x _____"

### No Answer Provided

If you don't provide an answer for the practice problem, the worksheet will show a long blank line for students to write the complete answer.

### Static Worksheets

Once generated, you can save the worksheet HTML and share it:
1. Generate your worksheet
2. View the page source (Ctrl+U / Cmd+U)
3. Copy the HTML
4. Save as a new .html file
5. Share with students

This creates a static worksheet that can be used without the generator.

## Printing Tips

### For Best Results

1. Use **Print to PDF** to save digitally
2. Select "Save as PDF" as your printer
3. Adjust margins if needed (usually default is fine)
4. Use Portrait orientation for most worksheets

### Print Settings

- **Margins**: Default or minimal
- **Background graphics**: Optional (adds color to sections)
- **Headers/Footers**: Turn off for cleaner look

## Troubleshooting

### Blank line not appearing?
- Check that your "Key Mistake Field" exactly matches part of the answer
- Include spaces if they're in the answer
- Case-sensitive matching

### Validation error?
- Bad Habit Description is required
- Example 1 Problem and Answer are required
- New Practice Problem is required
- Other fields are optional

### Print button not working?
- Use browser's print function (Ctrl+P / Cmd+P) instead
- Or right-click → Print

## Browser Compatibility

Works in all modern browsers:
- ✅ Chrome / Edge / Brave
- ✅ Firefox
- ✅ Safari
- ✅ Opera

No internet connection needed after first load!

## Getting Help

- Check `README.md` for overview
- View `example-fraction-addition.html` for a complete example
- Experiment with the pre-filled example in the form
