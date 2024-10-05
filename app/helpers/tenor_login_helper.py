from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import os

# Define the necessary scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/tenor']

# Function to handle OAuth2 flow and obtain the access token
def get_oauth2_token():
    # Initialize the OAuth flow using the client secret file
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/googleauth'  # Change port here

    # Run the local server to handle the OAuth flow
    creds = flow.run_local_server(port=8000)  # Use port 8080 or any available port
    return creds.token  # Return the access token

# Function to make an authenticated POST request using the obtained OAuth2 token
def make_authenticated_request():
    # Obtain the OAuth2 access token
    access_token = get_oauth2_token()

    # Set up the headers for the authenticated request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Origin': 'https://tenor.com',
        'Referer': 'https://tenor.com/'
    }

    # The POST request URL for registering the event with Tenor's API
    url_post = "https://tenor.googleapis.com/v2/registerevent"

    # The data for the POST request
    data_post = {
        'appversion': 'browser-r20240930-1',
        'prettyPrint': 'false',
        'key': 'AIzaSyC-P6_qz3FzCoXGLk6tgitZo4jEJ5mLzD8',  # API key for Tenor
        'client_key': 'tenor_web',
        'locale': 'en',
        'anon_id': 'AAYiA0ucCxAHxMlAjxQtuA',  # Example anonymous ID
        'eventname': 'signin_button_tap',
        'component': 'web_desktop',
        'current_uri': 'https://tenor.com/users/alan_hallow',  # Example user profile
        'data': '{"apirefid":"3c4b52e5-70d0-4b33-b29a-cd0418e8aad9","isUserLoggedIn":""}'
    }

    # Make the POST request using the requests library
    response = requests.post(url_post, headers=headers, data=data_post)

    # Check if the POST request was successful
    if response.status_code == 200:
        print('POST request successful:')
        print('Response:', response.json())
    else:
        print('POST request failed:')
        print('Status Code:', response.status_code)
        print('Response:', response.text)
