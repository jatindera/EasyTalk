# app/schemas/user_schemas.py

from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    provider_name: str
    provider_id: str
    role: str
