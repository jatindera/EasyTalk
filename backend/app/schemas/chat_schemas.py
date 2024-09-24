from pydantic import BaseModel
from typing import Optional

# Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    query: str
    chatSessionId: Optional[str] = None