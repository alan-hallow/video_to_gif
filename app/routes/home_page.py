from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

# Route for '/'
@router.get("/", response_class=HTMLResponse)
async def root():
    # Redirect to the /home route
    return RedirectResponse(url="/home")

# Route for '/home'
@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
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

    print(user_email, user_name, picture)

    # Pass the user data to the template
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "title": "Home", 
            "css": '../static/styles/home_page.css', 
            'username':user_name,
            'useremail':user_email,
            'userpicture': picture
        }
    )
