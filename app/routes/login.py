from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import db  # Import your MongoDB collection
from app.helpers.auth_helper import verify_password, create_access_token  # Assume these are your helper functions

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter()

# Login Page (GET)
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, response_class=HTMLResponse, error: str = None):
    return templates.TemplateResponse(
        "login.html", 
        {
            "request": request,
            "title": "Login",
            "css": "../static/styles/login_page.css",
            "error": error
        }
    )

# Handle login form submission (POST)
@router.post("/login", response_class=HTMLResponse)
async def handle_login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        # Query the user from the database
        user = await db.find_one({"email": email})  # Assuming MongoDB async driver

        # Check if the user exists and the password is valid
        if user and verify_password(password, user["hashed_password"]):
            # Generate JWT token for authentication
            token = create_access_token(data={"sub": str(user["_id"])})
            return RedirectResponse(
                url=f"/home?message=Welcome+{email}&token={token}",
                status_code=303
            )
        else:
            # Invalid credentials
            return RedirectResponse(
                url=f"/login?error=Invalid+credentials",
                status_code=303
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url="/login?error=An+unexpected+error+occurred",
            status_code=303
        )
