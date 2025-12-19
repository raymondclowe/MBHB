#!/usr/bin/env node

/**
 * Worksheet generator script - Called from Python backend
 * Usage: node generate_worksheet.js <data_json_file> <output_path>
 */

const fs = require('fs');
const { generateWorksheet, saveWorksheet } = require('./index');

async function main() {
    if (process.argv.length < 4) {
        console.error('Usage: node generate_worksheet.js <data_json_file> <output_path>');
        process.exit(1);
    }
    
    const dataFile = process.argv[2];
    const outputPath = process.argv[3];
    
    // Check for API key
    const apiKey = process.env.OPENROUTER_API_KEY;
    if (!apiKey) {
        console.error('Error: OPENROUTER_API_KEY environment variable not set');
        process.exit(1);
    }
    
    try {
        // Read worksheet data
        const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
        
        // Validate required fields
        if (!data.bad_habit || !data.example1 || !data.example2 || !data.problem) {
            console.error('Error: Missing required fields in data file');
            console.error('Required: bad_habit, example1, example2, problem');
            process.exit(1);
        }
        
        const { bad_habit, example1, example2, problem } = data;
        
        console.log('Generating worksheet...');
        console.log('Bad habit:', bad_habit);
        
        // Generate worksheet
        const html = await generateWorksheet(bad_habit, example1, example2, problem, apiKey);
        
        // Save worksheet
        saveWorksheet(html, outputPath);
        
        console.log('Worksheet generated successfully:', outputPath);
        process.exit(0);
        
    } catch (error) {
        console.error('Error generating worksheet:', error.message);
        process.exit(1);
    }
}

main();
