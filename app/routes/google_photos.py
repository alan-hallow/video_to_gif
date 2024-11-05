from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.google_photos_helper import process_google_photos
from fastapi.templating import Jinja2Templates
import json

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/home/google_photos", response_class=HTMLResponse)
async def google_photos_page(request: Request, gif_url_youtube: str = None, video_upload_message: str = None, error: str = None):
    # Retrieve the 'user_info' cookie
    user_info = request.cookies.get("user_info")
    
    if user_info:
        # Parse the JSON data from the cookie
        user_data = json.loads(user_info)
        user_email = user_data.get("email")
        user_name = user_data.get("name")
        picture = user_data.get("picture")
    else:
        user_email, user_name, picture = None, None, None

    return templates.TemplateResponse(
        "google_photos.html", 
        {
            "request": request,
            "title": "YouTube Video Upload",
            'css': '../static/styles/google_photos.css',
            'js': '../static/scripts/google_photos.js',
            "gif_url_youtube": gif_url_youtube,
            "video_upload_message": video_upload_message,
            "error": error,
            'username':user_name,
            'useremail':user_email,
            'userpicture': picture
        }
    )

@router.post('/input_google_photos_link', response_class=HTMLResponse)
async def handle_google_photos_upload(request: Request, video_link: str = Form(...)):
    try:
        result = await process_google_photos(video_link)
        if result["status"] == "success":
            gif_url_youtube = result["gif_url_youtube"]
            message = result["message"]
            return RedirectResponse(
                url=f"/home/google_photos?gif_url_youtube={gif_url_youtube}&video_upload_message={message}",
                status_code=303
            )
        else:
            error_message = result["message"]
            return RedirectResponse(
                url=f"/home/google_photos?error={error_message}",
                status_code=303
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/google_photos?error=An unexpected error occurred.",
            status_code=303
        )
