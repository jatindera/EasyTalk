from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    provider_name = Column(String(50))
    provider_id = Column(String(255))
    role = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Define the relationship to ChatSession
    chat_sessions = relationship("ChatSession", back_populates="user")  # This should match the ChatSession model's relationship
    # Define the relationship to ChatHistory
    chat_history = relationship("ChatHistory", back_populates="user")
