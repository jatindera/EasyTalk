from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Chat API"],
)

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
