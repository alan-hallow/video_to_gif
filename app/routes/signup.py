from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import users_collection  
# from app.helpers.auth_helper import hash_password, create_access_token
import json

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, error: str = None):
    
    # Retrieve cookies from the request
    user_email = request.cookies.get('email')
    user_name = request.cookies.get('name')
    picture = request.cookies.get('picture')
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
                'picture': picture
            }
        }
    )

@router.post("/signup", response_class=HTMLResponse)
async def handle_signup(request: Request, response: Response, name:str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    try:
        pass
        # if password != confirm_password:
        #     return RedirectResponse(
        #         url="/signup?error=Passwords+do+not+match", 
        #         status_code=303
        #     )

        # existing_user = await users_collection.find_one({"email": email})
        # if existing_user:
        #     return RedirectResponse(
        #         url="/signup?error=Email+already+registered", 
        #         status_code=303
        #     )
        
        # hashed_password = hash_password(password)
        # new_user = {
        #     "email": email,
        #     "hashed_password": hashed_password,
        #     "name": name  # Add a placeholder name for now, you can prompt for it in the form
        # }
        # await users_collection.insert_one(new_user)

        # token = create_access_token(data={"sub": str(new_user["_id"])})

        # # Create a cookie storing email and name
        # cookie_data = {
        #     "email": new_user["email"],
        #     "name": new_user["name"]
        # }
        # cookie_value = json.dumps(cookie_data)

        # # Set cookie
        # response = RedirectResponse(url="/home", status_code=303)
        # response.set_cookie(
        #     key="user_info", 
        #     value=cookie_value, 
        #     httponly=True, 
        #     secure=True, 
        #     samesite="Lax"
        # )

        # # Print the cookie value
        # print(f"Cookie set: user_info={cookie_value}")

        # return response

    except Exception as e:
        print(f"Unexpected error: {e}")
        return RedirectResponse(
            url="/signup?error=An+unexpected+error+occurred",
            status_code=303
        )

