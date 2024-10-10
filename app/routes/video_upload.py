from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.upload_video_helper import process_video_upload, process_video_upload_with_caption
from app.helpers.tenor_login_helper import make_authenticated_request 
from app.helpers.upload_tenor_helper import register_event_one, register_event_two, upload_gif
from app.helpers.upload_giphy_helper import upload_gif_to_giphy
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/home/upload_video", response_class=HTMLResponse)
async def upload_video_page(request: Request, gif_location: str = None, video_upload_message: str = None, error: str = None):
    # Retrieve cookies from the request
    user_email = request.cookies.get('email')
    user_name = request.cookies.get('name')
    picture = request.cookies.get('picture')

    return templates.TemplateResponse(
        "upload_video.html", 
        {
            "request": request,
            "title": "Upload Video",
            'css': '../static/styles/upload_video.css',
            "gif_location": gif_location,
            "video_upload_message": video_upload_message,
            "error": error,
            "user": {
                "email": user_email,
                "name": user_name,
                'picture': picture
            }
        }
    )

@router.post('/video_upload', response_class=HTMLResponse)
async def handle_video_upload(
    request: Request,
    upload_video: UploadFile = File(...),
    captions_bool: bool = Form(...),
    captions: str = Form(None),
    font_size: str = Form(None),
    boldness: str = Form(None),
    font_color_one: str = Form(None),
    font_color_two: str = Form(None),
    outline_color: str = Form(None),
    shadow_color: str = Form(None),
    shadow_offset: str = Form(None),
    line_spacing: str = Form(None),
    font: str = Form(None)
):
    try:
        # Process video upload with or without captions
        if captions_bool:
            result = await process_video_upload_with_caption(
                upload_video,
                captions,
                font_size,
                boldness,
                font_color_one,
                font_color_two,
                outline_color,
                shadow_color,
                shadow_offset="4,4",  # Default value
                line_spacing=10,       # Default value
                font="Oswald.ttf"      # Default font
            )
        else:
            result = await process_video_upload(upload_video)

        # Handle result based on status
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

@router.post('/upload_to_tenor')
async def upload_to_tenor(gif_location: str = Form(...)):
    try:
        # Tenor API logic
        result = make_authenticated_request()  # Removed 'await' since it's likely a synchronous function
        return {"message": "Successfully uploaded to Tenor", "result": result}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/upload_video?error=An unexpected error occurred.",
            status_code=303
        )

@router.post('/upload_to_giphy')
async def upload_to_giphy(request: Request, gif_location: str = Form(...)):
    try:
        # Dynamically get the file path for the GIF
        file_path = os.path.abspath(os.path.join(os.getcwd(), 'app', 'static', 'results', gif_location))
        print(file_path)

        tags = "funny, gif, new"
        source_post_url = None

        upload_gif_to_giphy(file_path=file_path, tags=tags, source_post_url=source_post_url)

        # Get the previous page from the Referer header
        referer_url = request.headers.get("Referer")
        if referer_url:
            return RedirectResponse(url=referer_url, status_code=303)
        else:
            return {"message": "Successfully uploaded to Giphy, but no referer URL found."}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/upload_video?error=An unexpected error occurred.",
            status_code=303
        )