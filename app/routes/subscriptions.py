from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/subscriptions", response_class=HTMLResponse)
async def subscriptions_page(request: Request):
    
    # Retrieve cookies from the request
    user_email = request.cookies.get('email')
    user_name = request.cookies.get('name')
    picture = request.cookies.get('picture')
    return templates.TemplateResponse("subscriptions.html", {"request": request, "title": "Subscriptions",
            "user": {
                "email": user_email,
                "name": user_name,
                'picture': picture
            }})
