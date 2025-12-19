/**
 * Example bad habits and templates for generating worksheets
 * Each example includes the bad habit, two worked examples, and a problem description
 */

const examples = [
  {
    name: "Negative Sign Distribution",
    badHabit: "Forgetting to distribute the negative sign when expanding -(a + b)",
    example1: "Simplify: -(3 + x). Correct: -3 - x. Common mistake: -3 + x",
    example2: "Simplify: -(5 - 2y). Correct: -5 + 2y. Common mistake: -5 - 2y",
    newProblem: "Expanding expressions with negative signs in front of parentheses"
  },
  {
    name: "Order of Operations",
    badHabit: "Doing addition/subtraction before multiplication/division (ignoring PEMDAS)",
    example1: "Calculate: 3 + 4 × 2. Correct: 3 + 8 = 11. Common mistake: 7 × 2 = 14",
    example2: "Calculate: 12 ÷ 3 + 2. Correct: 4 + 2 = 6. Common mistake: 12 ÷ 5 = 2.4",
    newProblem: "Mixed operations requiring proper order of operations"
  },
  {
    name: "Fraction Addition",
    badHabit: "Adding fractions by adding numerators and denominators separately (1/2 + 1/3 ≠ 2/5)",
    example1: "Add: 1/2 + 1/3. Correct: 3/6 + 2/6 = 5/6. Common mistake: 2/5",
    example2: "Add: 2/5 + 1/4. Correct: 8/20 + 5/20 = 13/20. Common mistake: 3/9 = 1/3",
    newProblem: "Adding fractions with different denominators"
  },
  {
    name: "Squaring Binomials",
    badHabit: "Thinking (a + b)² = a² + b² instead of a² + 2ab + b²",
    example1: "Expand: (x + 3)². Correct: x² + 6x + 9. Common mistake: x² + 9",
    example2: "Expand: (2y + 1)². Correct: 4y² + 4y + 1. Common mistake: 4y² + 1",
    newProblem: "Expanding squared binomial expressions"
  },
  {
    name: "Canceling Terms",
    badHabit: "Incorrectly canceling terms across addition (e.g., (x+3)/x ≠ 3)",
    example1: "Simplify: (x+5)/x. Correct: Cannot simplify (or 1 + 5/x). Common mistake: 5",
    example2: "Simplify: (2x+4)/(2x). Correct: 1 + 2/x. Common mistake: 4 or 2",
    newProblem: "Simplifying algebraic fractions with addition in numerator"
  }
];

module.exports = examples;
