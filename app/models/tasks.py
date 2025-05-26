from pydantic import BaseModel
from typing import List, Optional

class Demographics(BaseModel):
    age: int
    education: str
    familiarity_with_cognitive_science: str

class CRTTask(BaseModel):
    question: str
    answer: Optional[str] = None
    response_time: Optional[float] = None
    edits: Optional[int] = 0

class StroopTask(BaseModel):
    color_word: str
    font_color: str
    selected_color: Optional[str] = None
    response_time: Optional[float] = None
    correct: Optional[bool] = None

class DelayDiscountingTask(BaseModel):
    smaller_reward: float
    larger_reward: float
    choice: Optional[str] = None  # 'smaller' or 'larger'
    response_time: Optional[float] = None

class ConsistencyCheck(BaseModel):
    original_question: str
    modified_question: str
    original_answer: Optional[str] = None
    modified_answer: Optional[str] = None
    response_time: Optional[float] = None
    consistent: Optional[bool] = None