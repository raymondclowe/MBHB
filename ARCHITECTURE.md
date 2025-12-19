# MBHB Architecture

## System Overview

MBHB (Math Bad Habit Breaker) is a Node.js application that generates educational worksheets using AI. The system follows a simple three-stage pipeline:

```
Input (Bad Habit + Examples) → AI Generation (OpenRouter/Gemini) → Output (HTML Worksheet)
```

## Components

### 1. Core Module (`index.js`)

**Purpose**: Main application logic and API integration

**Key Functions**:
- `createPrompt(badHabit, example1, example2, newProblem)` - Constructs the AI prompt
- `generateWorksheet(...)` - Calls OpenRouter API to generate HTML
- `saveWorksheet(html, path)` - Saves generated HTML to file

**Dependencies**:
- `axios` - HTTP client for API calls

**API Integration**:
- Endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Model: `google/gemini-2.0-flash-exp:free`
- Authentication: Bearer token via `OPENROUTER_API_KEY`

### 2. Interactive CLI (`cli.js`)

**Purpose**: User-friendly command-line interface

**Features**:
- Menu-driven selection from pre-configured examples
- Custom input mode for user-defined bad habits
- Real-time feedback and progress display

**Dependencies**:
- `readline` - For interactive prompts
- `./index.js` - Core functionality
- `./examples.js` - Example configurations

### 3. Examples Library (`examples.js`)

**Purpose**: Pre-configured bad habit templates

**Structure**:
```javascript
{
  name: "Human-readable name",
  badHabit: "Description of the bad habit",
  example1: "First worked example",
  example2: "Second worked example",
  newProblem: "Problem type description"
}
```

**Current Examples**:
1. Negative Sign Distribution
2. Order of Operations
3. Fraction Addition
4. Squaring Binomials
5. Canceling Terms

### 4. Test Suite (`test.js`)

**Purpose**: Automated validation of system components

**Test Coverage**:
- File existence checks
- Module structure validation
- Example data integrity
- Prompt generation
- Sample worksheet validation
- Output directory creation

### 5. Sample Worksheet (`sample-worksheet.html`)

**Purpose**: Reference implementation and documentation

**Key Features**:
- Self-contained HTML/CSS/JavaScript
- No external dependencies
- Printable design
- Dynamic question generation
- Answer sheet functionality

## Data Flow

### Generation Process

1. **Input Collection**
   - User selects example or provides custom input
   - System validates required fields

2. **Prompt Construction**
   - `createPrompt()` builds detailed AI prompt
   - Includes instructions for HTML structure
   - Specifies JavaScript requirements
   - Defines progressive difficulty pattern

3. **AI Generation**
   - `generateWorksheet()` sends prompt to OpenRouter
   - Gemini 2.0 Flash processes request
   - Returns complete HTML document

4. **Post-Processing**
   - Extracts HTML from markdown code blocks (if present)
   - Validates basic structure

5. **Output**
   - `saveWorksheet()` creates timestamped file
   - Saves to `output/` directory
   - Returns file path to user

### Generated Worksheet Structure

```
HTML Document
├── Head
│   ├── Meta tags
│   └── Inline CSS styles
└── Body
    ├── Header (Title + Subtitle)
    ├── Bad Habit Explanation (Red box)
    ├── Worked Examples (Blue boxes × 2)
    ├── Practice Questions (Gray boxes × 10-13)
    │   ├── Easy questions (blanks in key fields)
    │   ├── Medium questions (multiple blanks)
    │   ├── Hard questions (complete solution needed)
    │   └── Trick questions (interspersed, marked with *)
    ├── Show Answers Button
    ├── Answer Sheet (Initially hidden)
    └── JavaScript
        ├── Question templates with generate() functions
        ├── displayQuestions() - Renders questions on page load
        ├── showAnswers() - Reveals answer sheet
        └── Mathematical calculations (using eval() or Function)
```

## AI Prompt Engineering

### Prompt Structure

The prompt sent to Gemini includes:

1. **Role Definition**: "You are an expert math education worksheet generator"
2. **Context**: Bad habit, examples, and problem description
3. **Output Requirements**:
   - HTML structure specifications
   - JavaScript functionality requirements
   - Progressive difficulty pattern
   - Trick question requirements
4. **Technical Constraints**:
   - Use eval() for calculations (with security note)
   - Self-contained (no external resources)
   - Printable design
5. **Formatting Instructions**: Output only HTML, no explanations

### Prompt Effectiveness

The prompt is designed to:
- Generate consistent, high-quality output
- Ensure mathematical accuracy through dynamic calculations
- Create pedagogically sound progression
- Include variety through trick questions
- Produce print-ready materials

## Security Considerations

### eval() Usage

**Context**: Generated worksheets use `eval()` for mathematical calculations

**Safety Measures**:
- Only AI-generated expressions are evaluated
- No user input is passed to eval()
- Worksheets are static files (generated once)
- All code is embedded at generation time

**Alternatives Considered**:
- `Function` constructor (also mentioned in prompt)
- Mathematical expression parsers (adds complexity/dependencies)
- Pre-calculated values (reduces flexibility)

**Recommendation**: Current approach is safe for the use case because:
1. The generator, not end users, controls the code
2. Worksheets are reviewed before distribution
3. No runtime user input is involved
4. The educational benefit outweighs theoretical risks

### API Key Security

**Storage**: Environment variable (`OPENROUTER_API_KEY`)
**Transmission**: HTTPS only
**Best Practices**:
- Never commit `.env` file (included in `.gitignore`)
- Use `.env.example` as template
- Document key acquisition process

## Design Decisions

### Why OpenRouter + Gemini?

1. **OpenRouter Advantages**:
   - Single API for multiple models
   - Free tier available (Gemini 2.0 Flash)
   - Good documentation
   - Rate limiting handled

2. **Gemini 2.0 Flash Benefits**:
   - Free to use
   - Good at following complex instructions
   - Generates clean HTML/JavaScript
   - Fast response times

### Why Self-Contained HTML?

1. **Portability**: Works offline, no hosting needed
2. **Simplicity**: No build process or bundlers
3. **Distribution**: Easy to share via email, LMS, etc.
4. **Privacy**: No external tracking or analytics
5. **Reliability**: Won't break if external resources disappear

### Why Progressive Blanking?

Educational research supports:
- **Scaffolding**: Start with support, gradually remove
- **Spaced Repetition**: Multiple attempts at similar problems
- **Metacognition**: Students self-assess understanding
- **Trick Questions**: Ensure conceptual understanding, not just pattern matching

## Extension Points

### Adding New Examples

1. Edit `examples.js`
2. Add new object with required fields
3. Test with `npm test`
4. Verify generated output

### Custom Models

To use different AI models:

1. Change `MODEL` constant in `index.js`
2. Update prompt if model has different capabilities
3. Test with several examples

### Custom Styling

Generated worksheets include inline CSS that can be:
1. Extracted to external stylesheet
2. Customized per-generation
3. Themed for different institutions

### Internationalization

Current implementation is English-only. To add i18n:

1. Externalize prompt strings
2. Add language parameter to `generateWorksheet()`
3. Provide language-specific examples
4. Update prompts to request output in target language

## Performance Considerations

### Generation Time

- API call: 3-10 seconds (network + AI processing)
- Post-processing: <100ms
- File save: <50ms
- **Total**: 5-15 seconds per worksheet

### Optimization Strategies

1. **Batch Generation**: Generate multiple worksheets in parallel
2. **Caching**: Store commonly used worksheets
3. **Template Pre-generation**: Create templates, fill in values client-side
4. **Model Selection**: Balance cost/speed/quality based on use case

### Costs

- **Free Tier**: ~0 cost with Gemini 2.0 Flash free model
- **Paid Models**: ~$0.001-0.01 per worksheet (varies by model)
- **Recommended**: Start with free, upgrade if quality issues

## Testing Strategy

### Current Tests

- Structural validation (files exist)
- Module exports verification
- Example data integrity
- Prompt generation
- Sample worksheet validation

### Future Test Ideas

1. **Integration Tests**: Full generation with mock API
2. **Output Validation**: Verify generated HTML structure
3. **Mathematical Correctness**: Validate calculations
4. **Browser Tests**: Automated UI testing with Playwright
5. **Accessibility Tests**: WCAG compliance checking

## Maintenance

### Regular Updates

1. **Dependencies**: Run `npm audit` and update packages
2. **API Changes**: Monitor OpenRouter changelog
3. **Model Updates**: Test with new Gemini versions
4. **Examples**: Add new bad habits based on user feedback

### Monitoring

Key metrics to track:
- Generation success rate
- Average generation time
- API costs (if using paid models)
- User feedback on worksheet quality

## Future Enhancements

### Potential Features

1. **Web UI**: Browser-based interface (no CLI needed)
2. **PDF Export**: Direct PDF generation
3. **Answer Key Separation**: Generate separate teacher/student versions
4. **Difficulty Levels**: User-configurable question difficulty
5. **Multi-language**: Support for non-English math education
6. **Question Bank**: Store and reuse generated questions
7. **Analytics**: Track which bad habits are most common
8. **Collaboration**: Share examples with community

### Architecture Evolution

As the system grows, consider:

1. **Modularization**: Split into npm packages
2. **Database**: Store generated worksheets and metadata
3. **Web Service**: API for generation requests
4. **Frontend**: React/Vue app for worksheet customization
5. **Authentication**: Multi-user support with accounts
