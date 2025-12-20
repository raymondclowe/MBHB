# MBHB Quick Start Guide

## 5-Minute Setup

### 1. Install (30 seconds)
```bash
git clone https://github.com/raymondclowe/MBHB.git
cd MBHB
npm install
```

### 2. Get API Key (2 minutes)
1. Go to [OpenRouter](https://openrouter.ai/keys)
2. Sign up (free)
3. Create an API key
4. Copy the key

### 3. Configure (10 seconds)
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### 4. Generate Worksheet (2 minutes)
```bash
npm run cli
```
- Select an example (1-5) or create custom (6)
- Wait 5-15 seconds for generation
- Open the generated HTML file in your browser

## Command Reference

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies |
| `npm start` | Generate default worksheet |
| `npm run cli` | Interactive mode (recommended) |
| `npm test` | Run tests |

## File Locations

| File | Purpose |
|------|---------|
| `output/*.html` | Generated worksheets |
| `sample-worksheet.html` | Example output |
| `examples.js` | Pre-configured examples |

## Troubleshooting

### Error: "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY="your-key"
echo $OPENROUTER_API_KEY  # Verify it's set
```

### Error: "npm not found"
Install Node.js from [nodejs.org](https://nodejs.org/)

### Worksheet won't open
- Make sure you're opening the `.html` file in a **web browser**
- Don't try to open it in a text editor
- Try a different browser (Chrome, Firefox, Safari)

### Generation takes too long
- Normal: 5-15 seconds
- Check internet connection
- Try again (API might be busy)

## Next Steps

1. ✅ Generate your first worksheet
2. 📖 Read [README.md](README.md) for overview
3. 📚 Read [USAGE.md](USAGE.md) for detailed guide
4. 🏗️ Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
5. 🎨 Customize examples in `examples.js`
6. 🚀 Share worksheets with students!

## Quick Tips

- **Review before distributing**: Always check AI-generated content
- **Print landscape**: Better layout for most worksheets
- **Separate answer sheets**: Print questions and answers separately
- **Reuse examples**: Save good worksheets for future use
- **Add your own**: Create custom bad habits in `examples.js`

## Common Use Cases

### Generate for classroom use
```bash
npm run cli
# Select example
# Print 30 copies
```

### Create custom worksheet
```bash
npm run cli
# Select option 6 (Custom)
# Enter your bad habit details
```

### Batch generate all examples
```bash
node -e "
const examples = require('./examples');
const { generateWorksheet, saveWorksheet } = require('./index');
const key = process.env.OPENROUTER_API_KEY;

(async () => {
  for (const ex of examples) {
    console.log('Generating:', ex.name);
    const html = await generateWorksheet(ex.badHabit, ex.example1, ex.example2, ex.newProblem, key);
    saveWorksheet(html, \`./output/\${ex.name.replace(/\\s+/g, '-')}.html\`);
  }
})();
"
```

## Support

- 📖 Documentation: README.md, USAGE.md, ARCHITECTURE.md
- 🐛 Issues: [GitHub Issues](https://github.com/raymondclowe/MBHB/issues)
- 💡 Examples: See `examples.js` for ideas

## Cost

- **Free**: Using Gemini 2.0 Flash free tier
- **Paid**: Optional, for higher quality (~$0.001 per worksheet)
- **No subscriptions**: Pay-per-use only

## Privacy

- ✅ No data collected
- ✅ No tracking
- ✅ Worksheets work offline
- ✅ API key stays on your machine
- ✅ Generated HTML has no external dependencies

---

**That's it!** You should now have a working Math Bad Habit Breaker system. 🎉
