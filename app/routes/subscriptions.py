from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/subscriptions", response_class=HTMLResponse)
async def subscriptions_page(request: Request):
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

    return templates.TemplateResponse("subscriptions.html", {"request": request, "title": "Subscriptions",
            'username':user_name,
            'useremail':user_email,
            'userpicture': picture
            
            })
