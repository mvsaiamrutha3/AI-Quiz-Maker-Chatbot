from typing import List, Dict, Any, Optional
import json
import docx
import io

from langchain.tools import tool
from langchain_openai import ChatOpenAI

import state  # <-- our global state container


# --- File Loading / Conversion (called directly from app.py) ---

def load_and_parse_json_string(file_content: str) -> Dict[str, Any]:
    try:
        return json.loads(file_content)
    except Exception as e:
        return {"error": f"Failed to parse JSON file: {e}"}


def convert_docx_to_quiz(file_stream: Any) -> Dict[str, Any]:
    try:
        document = docx.Document(io.BytesIO(file_stream.read()))
        full_text = "\n".join(p.text for p in document.paragraphs)
        if not full_text.strip():
            return {"error": "The DOCX file appears to be empty."}

        llm = ChatOpenAI(temperature=0, model="gpt-4o")
        prompt = (
            "Convert the following DOCX text into a JSON quiz with "
            "categories as keys and a 'questions' list under each. "
            "Each question needs 'question', 'options', and 'correct_option'.\n\n"
            f"{full_text}"
        )
        resp = llm.invoke(prompt)
        j = resp.content.strip().lstrip("```json").rstrip("```")
        return json.loads(j)
    except Exception as e:
        return {"error": f"Failed to process DOCX file: {e}"}


# --- Quiz‐editing tools, now using the global state.QUIZ_DATA ---


@tool
def add_new_question(
    category: str,
    question_text: str,
    options: List[str],
    correct_option: str
) -> Dict[str, Any]:
    """
    Appends a new question into state.QUIZ_DATA[category].
    """
    quiz = state.QUIZ_DATA
    if not quiz:
        return {"error": "No quiz loaded. Please load via JSON or DOCX first."}
    if category not in quiz:
        return {"error": f"Category '{category}' not found."}

    quiz[category]["questions"].append({
        "question": question_text,
        "options": options,
        "correct_option": correct_option,
        "points": 0,
        "type": "multiple-choice",
        "image": None
    })
    return quiz


@tool
def update_question(
    category: str,
    question_number: int,
    new_text: Optional[str] = None,
    new_options: Optional[List[str]] = None,
    new_correct_option: Optional[str] = None
) -> Dict[str, Any]:
    """
    Updates the specified question in place in state.QUIZ_DATA.
    """
    quiz = state.QUIZ_DATA
    try:
        q = quiz[category]["questions"][question_number - 1]
    except Exception as e:
        return {"error": f"Could not find question #{question_number} in '{category}': {e}"}

    if new_text:
        q["question"] = new_text
    if new_options:
        q["options"] = new_options
    if new_correct_option:
        opts = new_options or q["options"]
        if new_correct_option not in opts:
            return {"error": f"'{new_correct_option}' not in options list."}
        q["correct_option"] = new_correct_option

    return quiz


@tool
def delete_question(
    category: str,
    question_number: int
) -> Dict[str, Any]:
    """
    Deletes the specified question from state.QUIZ_DATA.
    """
    quiz = state.QUIZ_DATA
    try:
        del quiz[category]["questions"][question_number - 1]
        return quiz
    except Exception as e:
        return {"error": f"Could not delete question #{question_number} from '{category}': {e}"}
