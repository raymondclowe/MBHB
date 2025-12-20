#!/usr/bin/env python3
"""
Generate enhanced homework test fixtures from image analysis results.

This script processes analysis JSON files and creates or enhances homework
submission fixtures with realistic data extracted from actual student work.
"""
import json
from pathlib import Path
import sys
from datetime import datetime


# Get the project root directory
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"


def load_analysis_files():
    """Load all analysis JSON files from fixtures directory."""
    analysis_files = list(FIXTURES_DIR.glob("*.analysis.json"))

    analyses = []
    for analysis_file in sorted(analysis_files):
        try:
            with open(analysis_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Extract the content from OpenRouter response format
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]

                # Try to parse the content as JSON
                try:
                    # Remove markdown code blocks if present
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()

                    parsed_content = json.loads(content)

                    analyses.append(
                        {
                            "file": analysis_file.name,
                            "image": analysis_file.stem.replace(".analysis", ""),
                            "data": parsed_content,
                        }
                    )
                except json.JSONDecodeError:
                    print(f"  ⚠ Could not parse JSON from {analysis_file.name}")
                    # Store raw content for manual review
                    analyses.append(
                        {
                            "file": analysis_file.name,
                            "image": analysis_file.stem.replace(".analysis", ""),
                            "data": {"raw_content": content},
                        }
                    )
        except Exception as e:
            print(f"  ✗ Error loading {analysis_file.name}: {e}")

    return analyses


def generate_homework_from_analysis(analysis):
    """Generate a homework submission structure from analysis data."""
    data = analysis.get("data", {})
    image_name = analysis.get("image", "unknown")

    # Extract date from image filename if possible
    # Format: image_2025-12-19T13-03-39_user
    try:
        date_part = image_name.split("_")[1].split("T")[0]
        homework_date = date_part
    except (IndexError, ValueError):
        homework_date = datetime.now().strftime("%Y-%m-%d")

    # Generate student ID from image timestamp
    parts = image_name.split("_")
    student_id = f"IMG_{parts[1]}" if len(parts) > 1 else "IMG_UNKNOWN"

    homework = {
        "student_id": student_id,
        "student_name": f"Student from {image_name}",
        "homework_date": homework_date,
        "source_image": f"{image_name}.jpg",
        "questions": [],
    }

    # If we have parsed analysis data, use it
    if "raw_content" not in data:
        topic = data.get("topic", "Unknown Topic")
        difficulty = data.get("difficulty", "medium")
        mistakes = data.get("mistakes", [])
        problem_types = data.get("problem_types", [])
        question_numbers = data.get("question_numbers", [])

        # Generate questions based on analysis
        if not question_numbers:
            question_numbers = [1]  # Default to at least one question

        for i, q_num in enumerate(question_numbers):
            mistake_type = mistakes[i] if i < len(mistakes) else "general_error"
            problem_type = problem_types[i] if i < len(problem_types) else topic

            question = {
                "question_number": q_num if isinstance(q_num, int) else i + 1,
                "topic": problem_type,
                "difficulty": difficulty,
                "mistakes": [
                    {
                        "type": "error_from_image",
                        "description": (
                            mistake_type
                            if isinstance(mistake_type, str)
                            else str(mistake_type)
                        ),
                        "severity": "medium",
                    }
                ],
                "analysis": {
                    "ib_level": data.get("ib_level", "N/A"),
                    "student_understanding": data.get(
                        "student_understanding", "Requires review"
                    ),
                },
            }
            homework["questions"].append(question)

    return homework


def main():
    """Generate enhanced homework fixtures from all analysis files."""

    print("=" * 70)
    print("Generate Homework Fixtures from Image Analysis")
    print("=" * 70)
    print()

    if not FIXTURES_DIR.exists():
        print(f"❌ ERROR: Fixtures directory not found: {FIXTURES_DIR}")
        sys.exit(1)

    print(f"Fixtures directory: {FIXTURES_DIR}")
    print()

    # Load all analysis files
    print("Loading analysis files...")
    analyses = load_analysis_files()

    if not analyses:
        print("⚠ No analysis files found")
        print("  Run analyze_fixture_images.py first to generate analysis data")
        return

    print(f"Found {len(analyses)} analysis files")
    print()

    # Generate homework fixtures
    print("Generating homework fixtures...")
    print()

    generated_count = 0

    for analysis in analyses:
        try:
            homework = generate_homework_from_analysis(analysis)

            # Create filename based on image name
            image_name = analysis.get("image", "unknown")
            output_file = FIXTURES_DIR / f"homework_from_{image_name}.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(homework, f, indent=2, ensure_ascii=False)

            print(f"  ✓ Generated: {output_file.name}")
            generated_count += 1

        except Exception as e:
            print(f"  ✗ Error generating from {analysis.get('file', 'unknown')}: {e}")

    print()
    print("=" * 70)
    print("Generation Summary")
    print("=" * 70)
    print(f"Total analysis files: {len(analyses)}")
    print(f"Homework fixtures generated: {generated_count}")
    print()

    if generated_count > 0:
        print("✓ Homework fixtures generated successfully!")
    else:
        print("⚠ No homework fixtures were generated")


if __name__ == "__main__":
    main()
