from pydantic import BaseModel, Field
from typing import List, Optional, Any


class NoteCreate(BaseModel):
    subject: str = Field(..., min_length=1)
    title: Optional[str] = "Untitled Note"
    content: str = Field(..., min_length=10)


class AskRequest(BaseModel):
    question: str
    subject: Optional[str] = None


class FlashcardRequest(BaseModel):
    note_id: int
    count: int = 5


class QuizRequest(BaseModel):
    note_id: int
    difficulty: str = "medium"
    count: int = 5


class StudyPlanRequest(BaseModel):
    exam_date: str
    hours_per_day: int
    weak_topics: List[str] = []
    subjects: List[str] = []


class SummaryRequest(BaseModel):
    note_id: int