from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.youtube_channel_helper import process_youtube_channel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/home/youtube_channel", response_class=HTMLResponse)
async def youtube_channel_page(request: Request, gif_url_youtube: str = None, video_upload_message: str = None, error: str = None):
    # Retrieve cookies from the request
    user_email = request.cookies.get('email')
    user_name = request.cookies.get('name')
    picture = request.cookies.get('picture')
    return templates.TemplateResponse(
        "youtube_channel.html", 
        {
            "request": request,
            "title": "YouTube Video Upload",
            'css': '../static/styles/youtube_channel.css',
            'js': '../static/scripts/youtube_channel.js',
            "gif_url_youtube": gif_url_youtube,
            "video_upload_message": video_upload_message,
            "error": error,
            "user": {
                "email": user_email,
                "name": user_name,
                'picture': picture
            }
        }
    )

@router.post('/input_youtube_channel_link', response_class=HTMLResponse)
async def handle_youtube_video_upload(request: Request, channel_link: str = Form(...)):
    try:
        result = await process_youtube_channel(channel_link)
        if result["status"] == "success":
            gif_url_youtube = result["gif_url_youtube"]
            message = result["message"]
            return RedirectResponse(
                url=f"/home/youtube_channel?gif_url_youtube={gif_url_youtube}&video_upload_message={message}",
                status_code=303
            )
        else:
            error_message = result["message"]
            return RedirectResponse(
                url=f"/home/youtube_channel?error={error_message}",
                status_code=303
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/youtube_channel?error=An unexpected error occurred.",
            status_code=303
        )
