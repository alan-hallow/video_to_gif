from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import users_collection  # Use the 'users' collection
from app.helpers.auth_helper import hash_password, create_access_token  # Helper functions for hashing password and generating tokens
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter()

# Sign-up Page (GET)
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, error: str = None):
    return templates.TemplateResponse(
        "signup.html", 
        {
            "request": request,
            "title": "Sign Up",
            "css": "../static/styles/signup_page.css",
            "error": error
        }
    )

# Handle sign-up form submission (POST)
@router.post("/signup", response_class=HTMLResponse)
async def handle_signup(request: Request, email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    try:
        # Ensure the passwords match
        if password != confirm_password:
            return RedirectResponse(
                url="/signup?error=Passwords+do+not+match",
                status_code=303
            )

        # Check if the user already exists
        existing_user = await users_collection.find_one({"email": email})  # Query the 'users' collection
        if existing_user:
            return RedirectResponse(
                url="/signup?error=Email+already+registered",
                status_code=303
            )
        
        # Hash the user's password and save the user to the database
        hashed_password = hash_password(password)
        new_user = {
            "email": email,
            "hashed_password": hashed_password,
        }
        await users_collection.insert_one(new_user)  # Insert into 'users' collection

        # Generate JWT token for authentication
        token = create_access_token(data={"sub": str(new_user["_id"])})

        # Redirect to home page after successful sign-up
        return RedirectResponse(
            url=f"/home?message=Account+created+successfully&token={token}",
            status_code=303
        )

    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url="/signup?error=An+unexpected+error+occurred",
            status_code=303
        )
