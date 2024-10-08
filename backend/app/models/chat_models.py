from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
import uuid
from sqlalchemy.sql import func
from typing import List


class ChatHistory(Base):
    __tablename__ = "chat_history"

    message_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )  # Auto-generated message ID
    session_id = Column(
        String(36), ForeignKey("chat_sessions.session_id")
    )  # ForeignKey to ChatSession
    user_id = Column(
        String(255), ForeignKey("users.user_id"), nullable=True
    )  # User who initiated the query
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)  # Store message as JSON
    created_at = Column(DateTime, default=datetime.now)
    # Relationships
    chat_session = relationship("ChatSession", back_populates="chat_history")
    user = relationship("User", back_populates="chat_history")

    def __repr__(self):
        return f"<ChatHistory(id={self.id}, session_id={self.session_id}, user_id={self.user_id}, message={self.content}, created_at={self.created_at})>"


# Chat Session model
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    user_id = Column(String(255), ForeignKey("users.user_id"))
    session_name = Column(String(255), nullable=True)
    session_status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.now)

    # Relationship to link with user and chat history
    user = relationship("User", back_populates="chat_sessions")
    chat_history = relationship("ChatHistory", back_populates="chat_session")
