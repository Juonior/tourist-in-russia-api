from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    avatar_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    reviews = relationship("Review", back_populates="user")

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    main_photo_path = Column(String, nullable=True)  # Path to the main photo
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    reviews = relationship("Review", back_populates="place")
    photos = relationship("PlacePhoto", back_populates="place")

class PlacePhoto(Base):
    __tablename__ = "place_photos"

    id = Column(Integer, primary_key=True, index=True)
    photo_path = Column(String)  # Path to the photo
    place_id = Column(Integer, ForeignKey("places.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    place = relationship("Place", back_populates="photos")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    rating = Column(Integer)  # Rating from 1 to 10
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews") 