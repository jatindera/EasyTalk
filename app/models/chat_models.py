from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
import uuid


# Chat Session model
class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    session_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    session_name = Column(String(255), nullable=True)
    session_status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.now())
    
    # Relationship to link with user and chat history
    user = relationship("User", back_populates="chat_sessions")
    chat_history = relationship("ChatHistory", back_populates="chat_session")


class ChatHistory(Base):
    __tablename__ = 'chat_history'

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey('chat_sessions.session_id'))  # ForeignKey to ChatSession
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)  # User who initiated the query
    query = Column(Text, nullable=False)  # The query from the user
    answer = Column(Text, nullable=False)  # The AI-generated response
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp when the interaction occurred

    # Relationships
    chat_session = relationship("ChatSession", back_populates="chat_history")
    user = relationship("User", back_populates="chat_history")
