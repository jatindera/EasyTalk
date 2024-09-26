from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(String(255), primary_key=True, index=True, unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    ip_address = Column(String(255), nullable=False)
    provider_name = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    # Define the relationship to ChatSession
    chat_sessions = relationship("ChatSession", back_populates="user")  # This should match the ChatSession model's relationship
    # Define the relationship to ChatHistory
    chat_history = relationship("ChatHistory", back_populates="user")
