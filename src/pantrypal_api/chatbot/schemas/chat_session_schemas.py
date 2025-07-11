from typing import List, Optional

from pydantic import BaseModel


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    prep_time: Optional[int] = None
    instructions: List[str]
    ingredients: List[str]
    available_ingredients: int
    total_ingredients: int
