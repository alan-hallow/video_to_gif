from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.youtube_video_helper import process_youtube_video
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/home/youtube_video", response_class=HTMLResponse)
async def youtube_video_page(request: Request, gif_url_youtube: str = None, video_upload_message: str = None, error: str = None):
    return templates.TemplateResponse(
        "youtube_video.html", 
        {
            "request": request,
            "title": "YouTube Video Upload",
            'css': '../static/styles/youtube_video.css',
            'js': '../static/scripts/youtube_video.js',
            "gif_url_youtube": gif_url_youtube,
            "video_upload_message": video_upload_message,
            "error": error
        }
    )

@router.post('/input_youtube_video_link', response_class=HTMLResponse)
async def handle_youtube_video_upload(request: Request, video_link: str = Form(...)):
    try:
        result = await process_youtube_video(video_link)
        if result["status"] == "success":
            gif_url_youtube = result["gif_url_youtube"]
            message = result["message"]
            return RedirectResponse(
                url=f"/home/youtube_video?gif_url_youtube={gif_url_youtube}&video_upload_message={message}",
                status_code=303
            )
        else:
            error_message = result["message"]
            return RedirectResponse(
                url=f"/home/youtube_video?error={error_message}",
                status_code=303
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/youtube_video?error=An unexpected error occurred.",
            status_code=303
        )
