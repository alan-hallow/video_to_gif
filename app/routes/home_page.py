from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "home.html", 
        {"request": request, "title": "Home", 'css': '../static/styles/home_page.css'}
    )
