import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List  # Ensure List is imported for type hinting
from app.models.user_Model import user_Model
from app.db.db import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.schemas.user import UserLogin, Token
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=Token,tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    return user_service.authenticate_user(user, db)

@router.get("/protected",tags=["Auth"])
def protected_route(current_user: user_Model = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.username}!"}

@router.get("/users", response_model=List[UserResponse],tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = user_service.get_all_users(db)
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/users", response_model=UserResponse,tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)

@router.get("/users/{user_id}", response_model=UserResponse,tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse,tags=["Users"])
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(user_id, updated_user, db)

@router.delete("/users/{user_id}",tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(user_id, db)
    return {"message": "User deleted successfully"}
