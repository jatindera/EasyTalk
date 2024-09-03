from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import user_crud
from app.schemas import user_schemas


router = APIRouter(
    prefix="/users",
    tags=["users - API V1.0"],
)

@router.post("/users/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=user_schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
