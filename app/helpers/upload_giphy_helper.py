import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_gif_to_giphy(file_path, source_image_url=None, tags='None', source_post_url=None):
    # Get the API key from the .env file
    api_key = os.getenv('GIPHY_API_KEY')

    if not api_key:
        raise ValueError("API key not found. Make sure it's set in the .env file as GIPHY_API_KEY.")
    
    url = "https://upload.giphy.com/v1/gifs"
    
    # Define the payload with required parameters
    payload = {
        'api_key': api_key
    }
    
    # Add optional parameters if provided
    if tags:
        payload['tags'] = tags
    if source_post_url:
        payload['source_post_url'] = source_post_url

    # Check if a local file or source image URL is provided
    if file_path:
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, data=payload, files=files)
    elif source_image_url:
        payload['source_image_url'] = source_image_url
        response = requests.post(url, data=payload)
    else:
        raise ValueError("You must provide either a file path or source image URL")

    # Parse the response
    if response.status_code == 200:
        print("Upload successful!")
        print(response.json())
    else:
        print(f"Upload failed: {response.status_code}, {response.text}")
