from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

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
    # Retrieve cookies from the request
    user_email = request.cookies.get('email', None)
    user_name = request.cookies.get('name', None)
    picture = request.cookies.get('picture', None)

    # Pass the user data to the template
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "title": "Home", 
            "css": '../static/styles/home_page.css', 
            "user": {
                "email": user_email,
                "name": user_name,
                'picture': picture
            }
        }
    )
