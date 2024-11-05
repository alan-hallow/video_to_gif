from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import users_collection  
from app.helpers.auth_helper import hash_password, create_access_token
import json

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, error: str = None):
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

    return templates.TemplateResponse(
        "signup.html", 
        {
            "request": request,
            "title": "Sign Up",
            "css": "../static/styles/signup_page.css",
            "error": error,
            "user": {
                "email": user_email,
                "name": user_name,
                "picture": picture
            }
        }
    )

@router.post("/signup", response_class=HTMLResponse)
async def handle_signup(request: Request, response: Response, name: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    try:
        # Check if passwords match
        if password != confirm_password:
            return RedirectResponse(url="/signup?error=Passwords+do+not+match", status_code=303)

        # Check if user already exists
        existing_user = await users_collection.find_one({"email": email})
        if existing_user:
            return RedirectResponse(url="/signup?error=Email+already+registered", status_code=303)

        # Hash the password and create a new user
        hashed_password = hash_password(password)
        new_user = {
            "email": email,
            "hashed_password": hashed_password,
            "name": name
        }
        await users_collection.insert_one(new_user)

        # Create a token (optional)
        token = create_access_token(data={"sub": str(new_user["_id"])})

        # Store user info in a JSON object for the cookie
        cookie_data = {
            "email": new_user["email"],
            "name": new_user["name"],
            "picture": 'https://t4.ftcdn.net/jpg/02/29/75/83/360_F_229758328_7x8jwCwjtBMmC6rgFzLFhZoEpLobB6L8.jpg'
        }
        cookie_value = json.dumps(cookie_data)

        # Set the cookie with necessary properties
        response = RedirectResponse(url="/home", status_code=303)
        response.set_cookie(
            key="user_info", 
            value=cookie_value, 
            httponly=True, 
            secure=False,  # Set to False for local testing
            samesite="Lax"
        )

        print(f"Cookie set: user_info={cookie_value}")
        return response

    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(url="/signup?error=An+unexpected+error+occurred", status_code=303)
