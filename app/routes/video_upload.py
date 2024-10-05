from fastapi import APIRouter, Request, UploadFile, File, Form,  Header, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from app.helpers.upload_video_helper import process_video_upload, process_video_upload_with_caption

from app.helpers.tenor_login_helper import make_authenticated_request 
from app.helpers.upload_tenor_helper import register_event_one, register_event_two, upload_gif
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
        if captions_bool:

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



@router.post('/upload_to_tenor')
async def upload_to_tenor(gif_location: str = Form(...)):
    try:
        # Your logic to handle the GIF upload
        result = await make_authenticated_request()
        return {"message": "Successfully uploaded to Tenor", "result": result}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url=f"/home/upload_video?error=An unexpected error occurred.",
            status_code=303
        )

# @router.post("/upload_to_tenor")
# async def upload_to_tenor(gif_location: str = Form(...)):
#     try:
#         # Ensure gif_location is provided
#         if not gif_location:
#             raise HTTPException(status_code=400, detail="GIF location form data is required.")

#         print('Processing upload to Tenor...')

#         # Step 1: Authenticate with Tenor
#         access_token = await make_authenticated_request()  # Assuming this is async now

#         # Step 2: Execute async events and GIF upload
#         # result_one = await register_event_one()   # Uncomment if needed
#         # result_two = await register_event_two()   # Uncomment if needed
#         result_three = await upload_gif(gif_location, access_token)  # Assuming upload_gif is an async function that accepts the access token
        
#         # Extract the message from the GIF upload result
#         video_upload_message = result_three.get("message", "Upload completed")

#         # Redirect the user to the video upload page with success message
#         return RedirectResponse(
#             url=f"/home/upload_video?gif_location={gif_location}&video_upload_message={video_upload_message}",
#             status_code=303
#         )
#     except HTTPException as he:
#         print(f"HTTP error: {he.detail}")
#         return RedirectResponse(
#             url=f"/home/upload_video?error={he.detail}",
#             status_code=303
#         )
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return RedirectResponse(
#             url=f"/home/upload_video?error=An unexpected error occurred.",
#             status_code=303
#         )