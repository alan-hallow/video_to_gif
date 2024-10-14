# import os
# from fastapi import APIRouter, Request, HTTPException, Response
# from fastapi.responses import RedirectResponse
# from google_auth_oauthlib.flow import Flow
# from google.auth.transport.requests import Request as GoogleRequest
# from google.oauth2 import id_token
# from dotenv import load_dotenv
# from app.database import users_collection  # Assuming you have this setup like in signup
# from fastapi.responses import JSONResponse

# # Load environment variables
# load_dotenv()

# router = APIRouter()

# # Set up the Google OAuth 2.0 flow
# google_oauth_flow = Flow.from_client_secrets_file(
#     os.path.join(os.path.dirname(__file__), "../../client_secret.json"),  # Access client_secret.json from the root directory
#     scopes=[
#         "https://www.googleapis.com/auth/userinfo.profile",
#         "https://www.googleapis.com/auth/userinfo.email",
#         "openid"
#     ],
#     redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")  # Ensure this comes from .env
# )

# # Explicitly allow HTTP for development (insecure transport)
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Alternatively, set this in .env
# google_oauth_flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

# @router.get("/googleauth")
# def google_login():
#     """ Redirects the user to Google's OAuth 2.0 login page """
#     authorization_url, _ = google_oauth_flow.authorization_url(prompt='consent')
#     return RedirectResponse(url=authorization_url)

# @router.get("/auth/callback")
# async def google_callback(request: Request):
#     """ Handles the callback from Google after the user has signed in """
#     try:
#         google_oauth_flow.fetch_token(authorization_response=str(request.url))

#         # Verify and decode the ID token
#         credentials = google_oauth_flow.credentials
#         id_info = id_token.verify_oauth2_token(
#             credentials.id_token,
#             GoogleRequest(),
#             os.getenv("GOOGLE_CLIENT_ID")
#         )

#         # Extract relevant info about the user
#         user_info = {
#             "email": id_info["email"],
#             "name": id_info.get("name"),
#             "picture": id_info.get("picture")
#         }

#         # Print the extracted user information (email and name)
#         print(f"User Info: {user_info}")

#         # Store the user data in MongoDB
#         existing_user = await users_collection.find_one({"email": user_info["email"]})

#         if not existing_user:
#             # If user doesn't exist, insert the new user into MongoDB
#             new_user = {
#                 "email": user_info["email"],
#                 "name": user_info.get("name", "Unknown"),
#                 "picture": user_info.get("picture", None),  # Optionally store the user's profile picture
#             }
#             await users_collection.insert_one(new_user)
#             print(f"New user added to MongoDB: {new_user}")
#         else:
#             print(f"User already exists in MongoDB: {existing_user}")

#         # Set a cookie for the user (store email and name)
#         response = RedirectResponse(url="/home")  # Redirect to home after login
#         response.set_cookie(key="email", value=user_info["email"])
#         response.set_cookie(key="name", value=user_info.get("name", "Unknown"))
#         response.set_cookie(key="picture", value=user_info.get("picture", "Unknown"))

#         # Print confirmation of the cookie being set
#         print(f"Cookie set: email={user_info['email']}, name={user_info.get('name', 'Unknown')}, picture={user_info.get('picture', 'Unknown')}")

#         return response

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Google login error: {e}")





# @router.get('/signout')
# async def signout(request: Request, response: Response):
#     try:
#         # Clear the individual cookies with the same path as they were set
#         response.delete_cookie("email", path="/")
#         response.delete_cookie("name", path="/")
#         response.delete_cookie("picture", path="/")

#         print('Cookies are destroyed')

#         # Redirect to the home page after signing out
#         return RedirectResponse(url="/home", status_code=303)

#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return RedirectResponse(
#             url="/home?error=An+unexpected+error+occurred",
#             status_code=303
#         )
