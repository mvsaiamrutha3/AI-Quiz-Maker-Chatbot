# models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class QuizQuestion(BaseModel):
    """Data model for a single multiple-choice question."""
    question: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    correct_option: str
    points: int
    type: str = "multiple-choice"
    image: Optional[str] = None

class QuizCategory(BaseModel):
    """Data model for a category containing a list of questions."""
    questions: List[QuizQuestion]

class Quiz(BaseModel):
    """The root model for the entire quiz, mapping category names to their data."""
    quiz_data: Dict[str, QuizCategory]

