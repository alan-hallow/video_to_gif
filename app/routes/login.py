from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import users_collection  
# from app.helpers.auth_helper import verify_password, create_access_token
import json

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()



@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    
    # Retrieve cookies from the request
    user_email = request.cookies.get('email')
    user_name = request.cookies.get('name')
    picture = request.cookies.get('picture')
    return templates.TemplateResponse(
        "login.html", 
        {
            "request": request,
            "title": "Login",
            "css": "../static/styles/login_page.css",
            "error": error,
            "user": {
                "email": user_email,
                "name": user_name,
                'picture': picture
            }
        }
    )

@router.post("/login", response_class=HTMLResponse)
async def handle_login(request: Request, response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        pass
        # user = await users_collection.find_one({"email": email})

        # if user and verify_password(password, user["hashed_password"]):
        #     token = create_access_token(data={"sub": str(user["_id"])})

        #     # Create a cookie storing email and name (if available)
        #     cookie_data = {
        #         "email": user["email"],
        #         "name": user.get("name", "User")  # Use "User" if no name is in DB
        #     }
        #     cookie_value = json.dumps(cookie_data)

        #     # Set cookie
        #     response = RedirectResponse(url="/home", status_code=303)
        #     response.set_cookie(
        #         key="user_info", 
        #         value=cookie_value, 
        #         httponly=True, 
        #         secure=True, 
        #         samesite="Lax"
        #     )

        #     # Print the cookie value
        #     print(f"Cookie set: user_info={cookie_value}")

        #     return response
        # else:
        #     return RedirectResponse(
        #         url="/login?error=Invalid+credentials", 
        #         status_code=303
        #     )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url="/login?error=An+unexpected+error+occurred",
            status_code=303
        )
