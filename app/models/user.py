from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    provider = Column(String(50), nullable=True)
    provider_id = Column(String(255), nullable=True)
    role = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
