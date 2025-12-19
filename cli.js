#!/usr/bin/env node

/**
 * Interactive CLI for generating Math Bad Habit Breaker worksheets
 */

const readline = require('readline');
const { generateWorksheet, saveWorksheet } = require('./index');
const examples = require('./examples');
const path = require('path');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(prompt) {
  return new Promise((resolve) => {
    rl.question(prompt, resolve);
  });
}

async function main() {
  console.log('=== Math Bad Habit Breaker - Worksheet Generator ===\n');
  
  // Check for API key
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    console.error('Error: OPENROUTER_API_KEY environment variable not set');
    console.error('Please set your OpenRouter API key:');
    console.error('  export OPENROUTER_API_KEY="your-api-key-here"');
    console.error('\nGet your API key from: https://openrouter.ai/keys\n');
    process.exit(1);
  }

  // Show examples
  console.log('Available examples:');
  examples.forEach((ex, idx) => {
    console.log(`${idx + 1}. ${ex.name}`);
  });
  console.log(`${examples.length + 1}. Custom (enter your own)\n`);

  const choice = await question('Select an option (1-' + (examples.length + 1) + '): ');
  const choiceNum = parseInt(choice);

  let badHabit, example1, example2, newProblem;

  if (choiceNum >= 1 && choiceNum <= examples.length) {
    // Use selected example
    const selected = examples[choiceNum - 1];
    badHabit = selected.badHabit;
    example1 = selected.example1;
    example2 = selected.example2;
    newProblem = selected.newProblem;
    
    console.log(`\nSelected: ${selected.name}`);
    console.log(`Bad Habit: ${badHabit}\n`);
  } else if (choiceNum === examples.length + 1) {
    // Custom input
    console.log('\n=== Enter Custom Bad Habit Information ===\n');
    badHabit = await question('Bad habit to address: ');
    example1 = await question('Example 1 (with correct and incorrect): ');
    example2 = await question('Example 2 (with correct and incorrect): ');
    newProblem = await question('Problem description: ');
  } else {
    console.log('Invalid choice');
    rl.close();
    process.exit(1);
  }

  console.log('\nGenerating worksheet...');
  
  try {
    const html = await generateWorksheet(badHabit, example1, example2, newProblem, apiKey);
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outputPath = path.join(__dirname, 'output', `worksheet-${timestamp}.html`);
    
    saveWorksheet(html, outputPath);
    
    console.log('\n✓ Worksheet generated successfully!');
    console.log('✓ Open the file in a web browser to view and print.');
    console.log(`\nFile location: ${outputPath}`);
  } catch (error) {
    console.error('\n✗ Failed to generate worksheet:', error.message);
    process.exit(1);
  }
  
  rl.close();
}

main();
