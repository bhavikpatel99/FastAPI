from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from app.models.user_Model import user_Model
from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.config import settings

def authenticate_user(login_data: UserLogin, db: Session):
    user = db.query(user_Model).filter(user_Model.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

def create_user(user: UserCreate, db: Session):
    if db.query(user_Model).filter(user_Model.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(user_Model).filter(user_Model.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_pwd = hash_password(user.password)
    new_user = user_Model(
        username=user.username,
        email=user.email,
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(user_Model).all()

def get_user_by_id(user_id: int, db: Session):
    user = db.query(user_Model).filter(user_Model.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(user_id: int, updated_user: UserUpdate, db: Session):
    user = get_user_by_id(user_id, db)
    if updated_user.username:
        if db.query(user_Model).filter(user_Model.username == updated_user.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = updated_user.username
    if updated_user.email:
        if db.query(user_Model).filter(user_Model.email == updated_user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = updated_user.email
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    user = get_user_by_id(user_id, db)
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
