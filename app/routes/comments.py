from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.routes import auth
from app.database import get_db

router = APIRouter(prefix="/places/{place_id}/comments", tags=["comments"])

@router.post("/", response_model=schemas.Comment)
def create_comment(
    place_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    db_comment = models.Comment(
        content=comment.content,
        user_id=current_user.id,
        place_id=place_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/", response_model=List[schemas.Comment])
def read_comments(place_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.place_id == place_id).all()
    return comments 