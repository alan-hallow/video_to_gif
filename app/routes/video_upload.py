from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.upload_video_helper import process_video_upload
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/home/upload_video", response_class=HTMLResponse)
async def upload_video_page(request: Request, gif_location: str = None, video_upload_message: str = None, error: str = None):
    return templates.TemplateResponse(
        "upload_video.html", 
        {
            "request": request,
            "title": "Upload Video",
            'css': '../static/styles/upload_video.css',
            "gif_location": gif_location,
            "video_upload_message": video_upload_message,
            "error": error
        }
    )

@router.post('/video_upload', response_class=HTMLResponse)
async def handle_video_upload(request: Request, upload_video: UploadFile = File(...)):
    try:
        result = await process_video_upload(upload_video)
        if result["status"] == "success":
            gif_location = result["gif_location"]
            video_upload_message = result["message"]
            return RedirectResponse(
                url=f"/home/upload_video?gif_location={gif_location}&video_upload_message={video_upload_message}",
                status_code=303
            )
        else:
            error_message = result["message"]
            return RedirectResponse(
                url=f"/home/upload_video?error={error_message}",
                status_code=303
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/upload_video?error=An unexpected error occurred.",
            status_code=303
        )
