import json
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def _text_response(prompt: str) -> str:
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )
    return response.output_text.strip()


def summarize_note(content: str) -> str:
    prompt = f"""
You are a smart study assistant.
Summarize the following student note in a clean study-friendly format.

Return:
1. Short summary
2. Key concepts
3. Important facts
4. Quick revision tips

Note:
{content}
"""
    return _text_response(prompt)


def answer_question(question: str, contexts: List[str]) -> str:
    context_block = "\n\n".join(contexts) if contexts else "No context found."
    prompt = f"""
You are a note-grounded study assistant.

Rules:
- Answer using the provided study notes context.
- If the answer is partially missing, say what is available and mention the limitation.
- Be clear, structured, and student-friendly.

Question:
{question}

Context:
{context_block}
"""
    return _text_response(prompt)


def generate_flashcards(content: str, count: int = 5) -> list:
    prompt = f"""
Create {count} study flashcards from the note below.

Return ONLY valid JSON as an array of objects:
[
  {{"question": "...", "answer": "..."}}
]

Note:
{content}
"""
    raw = _text_response(prompt)
    return json.loads(raw)


def generate_quiz(content: str, difficulty: str = "medium", count: int = 5) -> dict:
    prompt = f"""
Create a {difficulty} quiz with {count} questions from the note below.

Return ONLY valid JSON in this format:
{{
  "title": "Quiz Title",
  "questions": [
    {{
      "type": "mcq",
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }},
    {{
      "type": "short",
      "question": "...",
      "answer": "..."
    }}
  ]
}}

Note:
{content}
"""
    raw = _text_response(prompt)
    return json.loads(raw)


def generate_study_plan(exam_date: str, hours_per_day: int, weak_topics: list, subjects: list) -> dict:
    prompt = f"""
You are a study planner assistant.

Create a practical day-wise study plan.

Inputs:
- Exam date: {exam_date}
- Hours per day: {hours_per_day}
- Weak topics: {weak_topics}
- Subjects: {subjects}

Return ONLY valid JSON:
{{
  "title": "Study Plan",
  "strategy": "...",
  "daily_plan": [
    {{
      "day": "Day 1",
      "focus": "...",
      "tasks": ["...", "..."],
      "revision": "..."
    }}
  ],
  "final_tips": ["...", "..."]
}}
"""
    raw = _text_response(prompt)
    return json.loads(raw)