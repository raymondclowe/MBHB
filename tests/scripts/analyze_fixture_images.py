#!/usr/bin/env python3
"""
Analyze student homework images using OpenRouter Gemini API.

This script processes all non-annotated student homework images in tests/fixtures/
and generates detailed analysis JSON files for use in testing.
"""
import requests
import os
import json
import base64
from pathlib import Path
import sys


OPENROUTER_API_KEY = os.environ.get("COPILOT_OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Get the project root directory (3 levels up from this script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"


def encode_image_to_base64(image_path):
    """Encode image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_image(image_path):
    """Send image to OpenRouter Gemini for analysis."""

    if not OPENROUTER_API_KEY:
        raise ValueError("COPILOT_OPENROUTER_API_KEY environment variable not set")

    # Read image and encode as base64
    image_base64 = encode_image_to_base64(image_path)
    image_ext = image_path.suffix.lower()

    # Determine MIME type
    mime_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
    mime_type = mime_types.get(image_ext, "image/jpeg")

    # Try gemini-3-pro-image-preview first, fall back to gemini-3-flash-preview
    models_to_try = [
        "google/gemini-3-pro-image-preview",
        "google/gemini-3-flash-preview",
    ]

    analysis_prompt = """Analyze this student homework image in detail. Provide:
    
1. Mathematical topic and IB HL AA Math level (if applicable)
2. Types of problems shown in the image
3. Common mistakes visible in the student work
4. Difficulty level (easy, medium, hard, very hard)
5. Educational context and commentary
6. Specific question numbers visible (if any)
7. Overall assessment of student understanding

Format your response as structured JSON with these keys:
{
  "topic": "string - main mathematical topic",
  "ib_level": "string - IB HL AA level or N/A",
  "problem_types": ["array of problem types shown"],
  "mistakes": ["array of specific mistakes observed"],
  "difficulty": "string - easy/medium/hard/very hard",
  "commentary": "string - educational assessment",
  "question_numbers": ["array of visible question numbers"],
  "student_understanding": "string - overall assessment"
}"""

    last_error = None

    for model in models_to_try:
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": analysis_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 2000,
            }

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/raymondclowe/MBHB",
                "X-Title": "MBHB CI Testing",
            }

            print(f"    Trying model: {model}")
            response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()

            # Check if we got a valid response
            if "choices" in result and len(result["choices"]) > 0:
                return result
            else:
                last_error = f"No choices in response from {model}"
                print(f"    ⚠ {last_error}")
                continue

        except requests.exceptions.HTTPError as e:
            last_error = f"HTTP error with {model}: {e}"
            print(f"    ⚠ {last_error}")
            continue
        except (
            requests.exceptions.RequestException,
            json.JSONDecodeError,
            KeyError,
        ) as e:
            last_error = f"Error with {model}: {e}"
            print(f"    ⚠ {last_error}")
            continue

    # If we get here, all models failed
    raise Exception(f"All models failed. Last error: {last_error}")


def main():
    """Process all non-annotated images in fixtures."""

    print("=" * 70)
    print("OpenRouter Gemini Image Analysis - Student Homework")
    print("=" * 70)
    print()

    if not OPENROUTER_API_KEY:
        print("❌ ERROR: COPILOT_OPENROUTER_API_KEY environment variable not set")
        print("   Set the API key to enable image analysis:")
        print("   export COPILOT_OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)

    if not FIXTURES_DIR.exists():
        print(f"❌ ERROR: Fixtures directory not found: {FIXTURES_DIR}")
        sys.exit(1)

    print(f"Fixtures directory: {FIXTURES_DIR}")
    print(f"API endpoint: {API_URL}")
    print()

    # Find all image files
    image_extensions = [".jpg", ".jpeg", ".png"]
    image_files = []

    for ext in image_extensions:
        image_files.extend(FIXTURES_DIR.glob(f"image_*{ext}"))

    # Filter out annotated/assistant images
    user_images = [
        img
        for img in image_files
        if "_annotated" not in img.name and "_assistant" not in img.name
    ]

    if not user_images:
        print("⚠ No user images found to analyze")
        return

    print(f"Found {len(user_images)} user images to analyze")
    print()

    success_count = 0
    error_count = 0

    for image_file in sorted(user_images):
        print(f"Analyzing: {image_file.name}")

        try:
            result = analyze_image(image_file)

            # Save analysis to JSON
            output_file = image_file.with_suffix(".analysis.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"  ✓ Saved analysis to {output_file.name}")
            success_count += 1

        except Exception as e:
            print(f"  ✗ Error analyzing {image_file.name}: {e}")
            error_count += 1

        print()

    # Print summary
    print("=" * 70)
    print("Analysis Summary")
    print("=" * 70)
    print(f"Total images processed: {len(user_images)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")

    if error_count > 0:
        print()
        print("⚠ Some images failed to analyze. Check logs above for details.")
        sys.exit(1)
    else:
        print()
        print("✓ All images analyzed successfully!")


if __name__ == "__main__":
    main()
