#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs');
const path = require('path');

/**
 * Main application for generating Math Breakthrough Builder worksheets
 * Uses OpenRouter API to access Gemini 2.0 Flash for generating HTML/JavaScript worksheets
 */

// Configuration
const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions';
const MODEL = 'google/gemini-2.0-flash-exp:free'; // Using Gemini 2.0 Flash (free tier)

/**
 * Creates the AI prompt for generating the worksheet
 */
function createPrompt(badHabit, example1, example2, newProblem) {
  return `You are an expert math education worksheet generator. Create a self-contained HTML file with embedded JavaScript that helps students achieve breakthrough improvements in mathematics through targeted practice.

COMMON CHALLENGE TO ADDRESS: ${badHabit}

EXAMPLE 1: ${example1}

EXAMPLE 2: ${example2}

NEW PROBLEM TO WORK ON: ${newProblem}

Generate a complete, self-contained HTML file that:

1. **Explains the common challenge** at the top with clear description and why it's important to master
2. **Shows 2 worked examples** with the key field BLANKED OUT (use "______") so students must hand-write the correct value
3. **Generates 10 progressive practice questions** where:
   - First 3 questions: Only the key field is blank
   - Next 4 questions: Multiple intermediate steps are blank
   - Last 3 questions: Entire answer is blank (students must fill in complete solution)
4. **Includes 3 "trick" questions** (interspersed) that are similar but have different patterns to test understanding
5. **Has JavaScript that**:
   - Defines question templates as objects with calculation formulas
   - Uses eval() to compute actual numeric values when page loads
   - Generates randomized but valid question parameters
   - Creates a separate answer sheet (hidden by default, shown with a button)
   - Validates that all calculations are correct

The HTML should be printable and professional-looking with CSS styling. Title it "Math Breakthrough Builder".

IMPORTANT REQUIREMENTS:
- The JavaScript must use eval() or Function constructor for calculations to ensure answers are numerically correct
- NOTE: Only use eval() on internally generated mathematical expressions, never on user input
- Questions must use variables and formulas, not hardcoded numbers
- Include a "Show Answers" button that reveals the answer sheet on a new page/section
- Make it printer-friendly with proper page breaks
- Use clear formatting with boxes for student answers
- Label trick questions subtly (e.g., with an asterisk * and note at bottom)
- Use positive language: "Common Challenge" instead of "Bad Habit"

Output ONLY the complete HTML code, starting with <!DOCTYPE html> and ending with </html>. Do not include any explanatory text before or after the HTML.`;
}

/**
 * Calls OpenRouter API to generate the HTML worksheet
 */
async function generateWorksheet(badHabit, example1, example2, newProblem, apiKey) {
  const prompt = createPrompt(badHabit, example1, example2, newProblem);
  
  try {
    const response = await axios.post(
      OPENROUTER_API_URL,
      {
        model: MODEL,
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://github.com/raymondclowe/MBHB',
          'X-Title': 'Math Breakthrough Builder'
        }
      }
    );

    const htmlContent = response.data.choices[0].message.content;
    
    // Extract HTML if it's wrapped in markdown code blocks
    let cleanedHtml = htmlContent;
    if (htmlContent.includes('```html')) {
      const match = htmlContent.match(/```html\n([\s\S]*?)\n```/);
      if (match) {
        cleanedHtml = match[1];
      }
    } else if (htmlContent.includes('```')) {
      const match = htmlContent.match(/```\n([\s\S]*?)\n```/);
      if (match) {
        cleanedHtml = match[1];
      }
    }
    
    return cleanedHtml;
  } catch (error) {
    console.error('Error calling OpenRouter API:', error.response?.data || error.message);
    throw error;
  }
}

/**
 * Saves the generated HTML to a file
 */
function saveWorksheet(html, outputPath) {
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  fs.writeFileSync(outputPath, html, 'utf8');
  console.log(`Worksheet saved to: ${outputPath}`);
}

/**
 * Main execution function
 */
async function main() {
  // Check for API key
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    console.error('Error: OPENROUTER_API_KEY environment variable not set');
    console.error('Please set your OpenRouter API key:');
    console.error('  export OPENROUTER_API_KEY="your-api-key-here"');
    process.exit(1);
  }

  // Example usage - these can be customized or passed as command line arguments
  const badHabit = "Forgetting to distribute the negative sign when expanding -(a + b)";
  const example1 = "Simplify: -(3 + x). Correct: -3 - x. Common mistake: -3 + x";
  const example2 = "Simplify: -(5 - 2y). Correct: -5 + 2y. Common mistake: -5 - 2y";
  const newProblem = "Expanding expressions with negative signs in front of parentheses";

  console.log('Generating worksheet for bad habit:', badHabit);
  console.log('Using OpenRouter with model:', MODEL);
  
  try {
    const html = await generateWorksheet(badHabit, example1, example2, newProblem, apiKey);
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outputPath = path.join(__dirname, 'output', `worksheet-${timestamp}.html`);
    
    saveWorksheet(html, outputPath);
    
    console.log('\nWorksheet generated successfully!');
    console.log('Open the file in a web browser to view and print.');
  } catch (error) {
    console.error('Failed to generate worksheet:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { generateWorksheet, createPrompt, saveWorksheet };
