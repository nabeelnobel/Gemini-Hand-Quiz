import os
import csv
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate_mcqs_from_paragraph(paragraph, output_csv="output_mcqs.csv"):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-2.0-flash"

    prompt = f"""
From the paragraph below, generate **EXACTLY 4** multiple-choice questions (MCQs) in the following **raw CSV** format:

Question,Choice1,Choice2,Choice3,Choice4,Answer

Rules:
- Each line represents 1 question with maximum 5 words.
- Each "Answer" must be the number (1–4) of the correct choice.
- Each "Answer" has 1-2 words.
- DO NOT include explanations, labels, or extra formatting.

Output it as a list of strings in a JSON format, under the key "MCQs".

Paragraph:
\"\"\"{paragraph}\"\"\"
"""

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    generate_content_config = types.GenerateContentConfig(response_mime_type="application/json")
    response_text = ""
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=generate_content_config):
        response_text += chunk.text

    try:
        parsed = json.loads(response_text)
        lines = parsed.get("MCQs", [])
    except json.JSONDecodeError:
        lines = [line.strip() for line in response_text.strip().splitlines() if line.strip()]

    if not lines or not all("," in line for line in lines):
        raise ValueError("Invalid response format from Gemini")

    with open(output_csv, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Question", "Choice1", "Choice2", "Choice3", "Choice4", "Answer"])
        for line in lines:
            row = [col.strip() for col in line.split(",")]
            if len(row) == 6:
                writer.writerow(row)

    return output_csv
