from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import models
from app.database import engine
from app.routes import auth, places, reviews
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tourist in Russia")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for avatars and place photos
app.mount("/static/avatars", StaticFiles(directory="avatars"), name="avatars")
app.mount("/static/places", StaticFiles(directory="places"), name="places")

# Include routers
app.include_router(auth.router)
app.include_router(places.router)
app.include_router(reviews.router) 