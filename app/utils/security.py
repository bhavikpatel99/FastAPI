from datetime import datetime, timedelta
from jose import JWTError, ExpiredSignatureError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.db import get_db
from app.models.user_Model import user_Model
from app.utils.config import settings

# Setup OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Update token URL if needed

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(user_Model).filter(user_Model.user_id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password against hashed version
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Decode JWT token with logging and validation
def decode_access_token(token: str):
    import logging
    logger = logging.getLogger(__name__)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if "sub" not in payload:
            logger.warning("Token missing 'sub' claim")
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return payload
    except ExpiredSignatureError:
        logger.warning("Expired token attempt")
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        logger.warning("Invalid token attempt")
        raise HTTPException(status_code=401, detail="Invalid token")
