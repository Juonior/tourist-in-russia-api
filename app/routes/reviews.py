from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.routes import auth
from app.database import get_db

router = APIRouter(tags=["reviews"])

@router.post("/places/{place_id}/reviews", response_model=schemas.Review)
def create_review(
    place_id: int,
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Check if user already left a review for this place
    existing_review = db.query(models.Review).filter(
        models.Review.place_id == place_id,
        models.Review.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already left a review for this place")
    
    db_review = models.Review(
        content=review.content,
        rating=review.rating,
        user_id=current_user.id,
        place_id=place_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/places/{place_id}/reviews", response_model=List[schemas.Review])
def read_reviews(place_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.place_id == place_id).all()
    return reviews

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete reviews")
    
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit() 