from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()



import asyncio

# Route for '/process_payment'
@router.get("/process_payment", response_class=HTMLResponse)
async def root():
    # Add a 3-second delay
    await asyncio.sleep(3)
    # Redirect to the /home route
    return RedirectResponse(url="/home")
    



# Route for '/payments'
@router.get("/payments", response_class=HTMLResponse)
async def home_page(request: Request):
    # Retrieve cookies from the request
    user_email = request.cookies.get('email', None)
    user_name = request.cookies.get('name', None)
    picture = request.cookies.get('picture', None)

    # Pass the user data to the template
    return templates.TemplateResponse(
        "payments.html", 
        {
            "request": request, 
            "title": "payments", 
            "css": '../static/styles/payments.css', 
            "user": {
                "email": user_email,
                "name": user_name,
                'picture': picture
            }
        }
    )
