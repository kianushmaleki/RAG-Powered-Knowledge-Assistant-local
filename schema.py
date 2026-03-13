
from pydantic import BaseModel

class AssistantResponse(BaseModel):
    answer: str
    confidence: float