import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Define the necessary scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.email']

# Function to handle OAuth2 flow
def get_oauth2_token():
    creds = None
    if os.path.abspath(os.path.join('..','video_to_gif', 'app','helpers','client_secret.json')):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials, go through the OAuth2 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds.token

# Make the authenticated POST request using the OAuth2 token
def make_authenticated_request():
    access_token = get_oauth2_token()
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Origin': 'https://tenor.com',
        'Referer': 'https://tenor.com/'
    }

    # The POST request URL for the event
    url_post = "https://tenor.googleapis.com/v2/registerevent"

    # The data for the POST request
    data_post = {
        'appversion': 'browser-r20240930-1',
        'prettyPrint': 'false',
        'key': 'AIzaSyC-P6_qz3FzCoXGLk6tgitZo4jEJ5mLzD8',
        'client_key': 'tenor_web',
        'locale': 'en',
        'anon_id': 'AAYiA0ucCxAHxMlAjxQtuA',
        'eventname': 'signin_button_tap',
        'component': 'web_desktop',
        'current_uri': 'https://tenor.com/users/alan_hallow',
        'data': '{"apirefid":"3c4b52e5-70d0-4b33-b29a-cd0418e8aad9","isUserLoggedIn":""}'
    }

    # Make the POST request
    response = requests.post(url_post, headers=headers, data=data_post)

    # Check the response and print it
    if response.status_code == 200:
        print('POST request successful:')
        print('Response:', response.json())
    else:
        print('POST request failed:')
        print('Status Code:', response.status_code)
        print('Response:', response.text)

# Run the authenticated request
make_authenticated_request()


