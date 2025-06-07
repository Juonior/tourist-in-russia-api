from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfile(User):
    avatar_path: Optional[str] = None

    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PlacePhotoBase(BaseModel):
    photo_path: str

class PlacePhotoCreate(PlacePhotoBase):
    pass

class PlacePhoto(PlacePhotoBase):
    id: int
    place_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PlaceBase(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float
    main_photo_path: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class Place(PlaceBase):
    id: int
    created_at: datetime
    average_rating: Optional[float] = None
    photos: List[PlacePhoto] = []

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    content: str
    rating: int = Field(ge=1, le=10)

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    place_id: int
    created_at: datetime
    user: UserProfile

    class Config:
        from_attributes = True

class PlaceWithReviews(Place):
    reviews: List[Review] 