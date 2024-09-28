from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/subscriptions", response_class=HTMLResponse)
async def subscriptions_page(request: Request):
    return templates.TemplateResponse("subscriptions.html", {"request": request, "title": "Subscriptions"})
