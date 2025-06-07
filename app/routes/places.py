from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import shutil
import os
from app import models, schemas
from app.routes import auth
from app.database import get_db

router = APIRouter(prefix="/places", tags=["places"])

# Create directories if they don't exist
os.makedirs("places", exist_ok=True)
os.makedirs("places/main", exist_ok=True)
os.makedirs("places/gallery", exist_ok=True)

@router.post("/", response_model=schemas.Place)
def create_place(
    place: schemas.PlaceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create places")
    
    db_place = models.Place(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@router.post("/{place_id}/main-photo", response_model=schemas.Place)
async def upload_main_photo(
    place_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can upload photos")
    
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Save the file
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"places/main/{place_id}{file_extension}"
    static_path = f"/static/places/main/{place_id}{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update place with photo path
    place.main_photo_path = static_path
    db.commit()
    db.refresh(place)
    
    return place

@router.post("/{place_id}/photos", response_model=schemas.PlacePhoto)
async def upload_place_photo(
    place_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can upload photos")
    
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Save the file
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"places/gallery/{place_id}_{file.filename}"
    static_path = f"/static/places/gallery/{place_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create photo record
    db_photo = models.PlacePhoto(
        photo_path=static_path,
        place_id=place_id
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    
    return db_photo

@router.get("/", response_model=List[schemas.PlaceWithReviews])
def read_places(
    skip: int = 0, 
    limit: int = 100, 
    sort_by_rating: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(models.Place)
    
    if sort_by_rating:
        # Subquery to calculate average rating
        avg_rating = db.query(
            models.Review.place_id,
            func.avg(models.Review.rating).label('avg_rating')
        ).group_by(models.Review.place_id).subquery()
        
        # Join with the subquery and order by average rating
        query = query.outerjoin(
            avg_rating,
            models.Place.id == avg_rating.c.place_id
        ).order_by(avg_rating.c.avg_rating.desc().nullslast())
    
    places = query.offset(skip).limit(limit).all()
    
    # Calculate average rating for each place
    for place in places:
        avg_rating = db.query(func.avg(models.Review.rating)).filter(
            models.Review.place_id == place.id
        ).scalar()
        place.average_rating = float(avg_rating) if avg_rating else None
    
    return places

@router.get("/{place_id}", response_model=schemas.PlaceWithReviews)
def read_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Calculate average rating
    avg_rating = db.query(func.avg(models.Review.rating)).filter(
        models.Review.place_id == place.id
    ).scalar()
    place.average_rating = float(avg_rating) if avg_rating else None
    
    return place 

@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_place(
    place_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete places")
    
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Delete associated photos from filesystem
    if place.main_photo_path:
        main_photo_path = place.main_photo_path.replace("/static/", "")
        if os.path.exists(main_photo_path):
            os.remove(main_photo_path)
    
    # Delete gallery photos
    for photo in place.photos:
        photo_path = photo.photo_path.replace("/static/", "")
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    # Delete from database
    db.delete(place)
    db.commit() 