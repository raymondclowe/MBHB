/**
 * Example improvement areas and templates for generating worksheets
 * Each example includes the common challenge, two worked examples, and a problem description
 */

const examples = [
  {
    name: "Negative Sign Distribution",
    badHabit: "Distributing the negative sign when expanding -(a + b)",
    example1: "Simplify: -(3 + x). Correct: -3 - x. Watch for: -3 + x",
    example2: "Simplify: -(5 - 2y). Correct: -5 + 2y. Watch for: -5 - 2y",
    newProblem: "Expanding expressions with negative signs in front of parentheses"
  },
  {
    name: "Order of Operations",
    badHabit: "Applying proper order of operations (PEMDAS/BODMAS)",
    example1: "Calculate: 3 + 4 × 2. Correct: 3 + 8 = 11. Watch for: 7 × 2 = 14",
    example2: "Calculate: 12 ÷ 3 + 2. Correct: 4 + 2 = 6. Watch for: 12 ÷ 5 = 2.4",
    newProblem: "Mixed operations requiring proper order of operations"
  },
  {
    name: "Fraction Addition",
    badHabit: "Adding fractions with different denominators (need common denominator)",
    example1: "Add: 1/2 + 1/3. Correct: 3/6 + 2/6 = 5/6. Watch for: 2/5",
    example2: "Add: 2/5 + 1/4. Correct: 8/20 + 5/20 = 13/20. Watch for: 3/9 = 1/3",
    newProblem: "Adding fractions with different denominators"
  },
  {
    name: "Squaring Binomials",
    badHabit: "Expanding (a + b)² = a² + 2ab + b² (remembering the middle term)",
    example1: "Expand: (x + 3)². Correct: x² + 6x + 9. Watch for: x² + 9",
    example2: "Expand: (2y + 1)². Correct: 4y² + 4y + 1. Watch for: 4y² + 1",
    newProblem: "Expanding squared binomial expressions"
  },
  {
    name: "Canceling Terms",
    badHabit: "Understanding when terms can and cannot cancel in fractions",
    example1: "Simplify: (x+5)/x. Correct: Cannot simplify (or 1 + 5/x). Watch for: 5",
    example2: "Simplify: (2x+4)/(2x). Correct: 1 + 2/x. Watch for: 4 or 2",
    newProblem: "Simplifying algebraic fractions with addition in numerator"
  }
];

module.exports = examples;
