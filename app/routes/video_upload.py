from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.upload_video_helper import process_video_upload, process_video_upload_with_caption
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
async def handle_video_upload(request: Request, upload_video: UploadFile = File(...),captions_bool:bool = Form(...), captions: str = Form(...), font_size: str= Form(...), boldness: str= Form(...), font_color_one: str= Form(...), font_color_two: str= Form(...), outline_color: str= Form(...), shadow_color: str= Form(...), shadow_offset: str= Form(...), line_spacing: str= Form(...), font: str= Form(...)):
    try:
        if captions_bool ==  True:

            print("with captiueknfakjf")

            result = await process_video_upload_with_caption(upload_video, captions, font_size, boldness, font_color_one, font_color_two, outline_color, shadow_color, shadow_offset="4,4", line_spacing=10, font="Oswald.ttf")
        else:
            print(captions_bool)
            print('wekjfekj')
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
