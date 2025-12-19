# MBHB - Math Bad Habit Breaker

A worksheet generator that creates printable practice worksheets specifically designed to break bad math habits.

## Overview

This tool generates custom HTML worksheets that help students practice avoiding common mathematical mistakes. Each worksheet includes:

- A clear description of the bad habit to break
- An AI template prompt explaining the correct approach
- Two worked examples with blanked-out key mistake fields
- A practice problem for the student to complete

## How to Use

1. **Open the tool**: Open `index.html` in any web browser
2. **Fill in the form**:
   - **Bad Habit Description**: Describe the mathematical mistake students commonly make
   - **AI Template Prompt**: Provide guidance on the correct approach
   - **Example 1 & 2**: Give two example problems with:
     - The problem statement
     - The complete answer
     - The specific part that should be blanked out (the "key mistake field")
   - **New Practice Problem**: Add a fresh problem for students to practice
3. **Generate**: Click "Generate Worksheet" to create the printable worksheet
4. **Print**: Click the print button or use your browser's print function to create a physical worksheet

## Features

- **Pre-filled Example**: The form comes pre-loaded with an example about distributing negative signs
- **Blanked Fields**: The key mistake areas are replaced with blank lines for students to fill in by hand
- **Printable Format**: The worksheet is optimized for printing with a clean, professional layout
- **Reusable**: Click "Back to Form" to create additional worksheets

## Example Use Case

The default example addresses the common mistake of forgetting to distribute negative signs when expanding expressions like -(a+b). Students often write -(a+b) = -a+b instead of the correct -a-b.

## Technical Details

- Self-contained HTML/JavaScript file (no external dependencies)
- Works offline once downloaded
- Print-friendly CSS media queries hide form elements when printing
- Responsive design works on desktop and mobile browsers  
