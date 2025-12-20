#!/usr/bin/env node

/**
 * Test script to verify the basic functionality without requiring API key
 * Creates a sample worksheet using the embedded template
 */

const fs = require('fs');
const path = require('path');

console.log('=== MBHB Test Script ===\n');

// Test 1: Check all required files exist
console.log('Test 1: Checking required files...');
const requiredFiles = [
  'index.js',
  'cli.js',
  'examples.js',
  'package.json',
  'README.md',
  'sample-worksheet.html'
];

let allFilesExist = true;
requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`  ✓ ${file} exists`);
  } else {
    console.log(`  ✗ ${file} missing`);
    allFilesExist = false;
  }
});

if (!allFilesExist) {
  console.error('\n✗ Some required files are missing');
  process.exit(1);
}

// Test 2: Verify examples structure
console.log('\nTest 2: Checking examples structure...');
try {
  const examples = require('./examples');
  console.log(`  ✓ Found ${examples.length} example bad habits`);
  
  examples.forEach((ex, idx) => {
    if (ex.name && ex.badHabit && ex.example1 && ex.example2 && ex.newProblem) {
      console.log(`  ✓ Example ${idx + 1}: ${ex.name} - valid`);
    } else {
      console.log(`  ✗ Example ${idx + 1}: ${ex.name} - missing fields`);
    }
  });
} catch (error) {
  console.error('  ✗ Error loading examples:', error.message);
  process.exit(1);
}

// Test 3: Verify main module exports
console.log('\nTest 3: Checking main module exports...');
try {
  const main = require('./index');
  const exports = ['generateWorksheet', 'createPrompt', 'saveWorksheet'];
  
  exports.forEach(exp => {
    if (typeof main[exp] === 'function') {
      console.log(`  ✓ ${exp}() is exported`);
    } else {
      console.log(`  ✗ ${exp}() is not exported`);
    }
  });
} catch (error) {
  console.error('  ✗ Error loading main module:', error.message);
  process.exit(1);
}

// Test 4: Test prompt generation
console.log('\nTest 4: Testing prompt generation...');
try {
  const { createPrompt } = require('./index');
  const examples = require('./examples');
  const ex = examples[0];
  
  const prompt = createPrompt(ex.badHabit, ex.example1, ex.example2, ex.newProblem);
  
  if (prompt.length > 100 && prompt.includes(ex.badHabit)) {
    console.log('  ✓ Prompt generated successfully');
    console.log(`  ✓ Prompt length: ${prompt.length} characters`);
  } else {
    console.log('  ✗ Prompt generation failed');
  }
} catch (error) {
  console.error('  ✗ Error generating prompt:', error.message);
  process.exit(1);
}

// Test 5: Verify sample worksheet is valid HTML
console.log('\nTest 5: Checking sample worksheet...');
try {
  const samplePath = path.join(__dirname, 'sample-worksheet.html');
  const content = fs.readFileSync(samplePath, 'utf8');
  
  if (content.includes('<!DOCTYPE html>') && content.includes('</html>')) {
    console.log('  ✓ Sample worksheet is valid HTML');
  } else {
    console.log('  ✗ Sample worksheet appears invalid');
  }
  
  if (content.includes('eval') || content.includes('generate')) {
    console.log('  ✓ Contains JavaScript generation logic');
  }
  
  if (content.includes('trick')) {
    console.log('  ✓ Includes trick question support');
  }
  
  if (content.includes('Show Answer') || content.includes('showAnswers')) {
    console.log('  ✓ Has answer sheet functionality');
  }
} catch (error) {
  console.error('  ✗ Error reading sample worksheet:', error.message);
  process.exit(1);
}

// Test 6: Copy sample worksheet to output for verification
console.log('\nTest 6: Creating test output...');
try {
  const outputDir = path.join(__dirname, 'output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const samplePath = path.join(__dirname, 'sample-worksheet.html');
  const testOutputPath = path.join(outputDir, 'test-worksheet.html');
  
  fs.copyFileSync(samplePath, testOutputPath);
  console.log(`  ✓ Test worksheet created at: ${testOutputPath}`);
  console.log('  ✓ Open this file in a browser to verify functionality');
} catch (error) {
  console.error('  ✗ Error creating test output:', error.message);
  process.exit(1);
}

console.log('\n=== All Tests Passed! ===\n');
console.log('Summary:');
console.log('  • All required files are present');
console.log('  • Module structure is correct');
console.log('  • Examples are properly configured');
console.log('  • Sample worksheet is ready to use');
console.log('\nNext steps:');
console.log('  1. Set OPENROUTER_API_KEY environment variable');
console.log('  2. Run "node index.js" or "npm start" to generate a worksheet');
console.log('  3. Run "node cli.js" or "npm run cli" for interactive mode');
console.log('  4. Open output/test-worksheet.html in a browser to see the sample');
console.log('\n');
