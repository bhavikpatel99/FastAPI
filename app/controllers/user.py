from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.item import Item  # Import the ORM model

router = APIRouter()

@router.get("/users")
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items