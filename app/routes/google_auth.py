from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter()

# Load environment variables from .env file
config = Config(".env")

# Initialize OAuth
oauth = OAuth(config)

# Register Google OAuth provider
oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    client_kwargs={'scope': 'openid profile email'},
)

# Google auth route
@router.get('/google_auth')
async def google_auth(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# OAuth callback route
@router.get('/auth')
async def auth(request: Request):
    try:
        # Get the OAuth token
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        # Error handling
        return templates.TemplateResponse(
            name="error.html",
            context={'request': request, 'error': e.error}
        )

    # Extract user info from token
    user = token.get('userinfo')
    if user:
        # Store user information in session
        request.session['user'] = dict(user)

    # Render home page with user info
    return templates.TemplateResponse(
        name='home.html',
        context={'request': request, 'user': dict(user)}
    )
