import os
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from app.database import db
from fastapi.templating import Jinja2Templates

# Import routers
from app.routes import home_page
from app.routes import login  
from app.routes import signup
from app.routes import video_upload
from app.routes import youtube_video
from app.routes import youtube_channel
from app.routes import google_photos
from app.routes import subscriptions




# Load environment variables
load_dotenv()

# Setup FastAPI app instance
app = FastAPI(debug=os.getenv("DEBUG", True))

# Set up template directory for HTML files
templates = Jinja2Templates(directory="app/templates")

# Mount static files (like CSS) for use in the app
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# MongoDB connection
users_collection = db["users"]  # Asynchronous MongoDB access

# Register routers
app.include_router(login.router)
app.include_router(signup.router)
app.include_router(home_page.router)
app.include_router(video_upload.router)
app.include_router(youtube_video.router)
app.include_router(google_photos.router)
app.include_router(youtube_channel.router)
app.include_router(subscriptions.router)

# Add additional middlewares or customizations if needed
