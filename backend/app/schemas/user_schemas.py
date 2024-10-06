# app/schemas/user_schemas.py

from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    ip_address: str
    provider_name: str
    role: str
