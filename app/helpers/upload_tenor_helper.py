import os
import requests

async def register_event_one():
    # Define the full URL with the query parameters included
    url = "https://tenor.googleapis.com/v2/registerevent?appversion=browser-r20240917-1&prettyPrint=false&key=AIzaSyC-P6_qz3FzCoXGLk6tgitZo4jEJ5mLzD8&client_key=tenor_web&locale=en&eventname=upload_start_tap&component=web_desktop&current_uri=https%3A%2F%2Ftenor.com%2Fgif-maker%3Futm_source%3Dnav-bar%26utm_medium%3Dinternal%26utm_campaign%3Dgif-maker-entrypoints&upload_profile_id=3545430206020164202&api_version=API_V2&data=%7B%22viewindex%22%3A1%2C%22apirefid%22%3A%226afaa7ec-7246-4b54-8db3-4b4e5a4a05a9%22%7D"
    
    # Define the headers as provided
    headers = {
        "Host": "tenor.googleapis.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://tenor.com/",
        "Content-Type": "application/x-www-form-urlencoded",  # Using form-url-encoded as mentioned
        "Origin": "https://tenor.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=0",
        "TE": "trailers",
        "Content-Length": "0"  # No body content
    }

    # Make the POST request
    response = requests.post(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        print('Event registered successfully')
        print('Response:', response.json())
    else:
        print("Failed to register event")
        print("Status Code:", response.status_code)
        print("Response:", response.text)





async def register_event_two():
    # Define the full URL with the query parameters included
    url = "https://tenor.googleapis.com/v2/registerevent?appversion=browser-r20240917-1&prettyPrint=false&key=AIzaSyC-P6_qz3FzCoXGLk6tgitZo4jEJ5mLzD8&client_key=tenor_web&locale=en&eventname=upload&component=web_desktop&current_uri=https%3A%2F%2Ftenor.com%2Fgif-maker%3Futm_source%3Dnav-bar%26utm_medium%3Dinternal%26utm_campaign%3Dgif-maker-entrypoints&upload_profile_id=3545430206020164202&api_version=API_V2&data=%7B%22upload_session_id%22%3A%221ehwoxqk9wz%22%2C%22category%22%3A%22file_gif%22%2C%22actions%22%3A%22%22%2C%22apirefid%22%3A%226afaa7ec-7246-4b54-8db3-4b4e5a4a05a9%22%7D"
    
    # Define the headers as provided
    headers = {
        "Host": "tenor.googleapis.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://tenor.com/",
        "Content-Type": "application/x-www-form-urlencoded",  # Using form-url-encoded as mentioned
        "Origin": "https://tenor.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=0",
        "Content-Length": "0",  # No body content
        "TE": "trailers"
    }

    # Make the POST request
    response = requests.post(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        print('Event registered successfully')
        print('Response:', response.json())
    else:
        print("Failed to register event")
        print("Status Code:", response.status_code)
        print("Response:", response.text)




async def upload_gif(gif_location):
    # Define the full URL with the query parameters included
    url = "https://tenor.googleapis.com/upload/v2/upload?appversion=browser-r20240917-1&prettyPrint=false&key=AIzaSyC-P6_qz3FzCoXGLk6tgitZo4jEJ5mLzD8&client_key=tenor_web&locale=en&tags=bird%2Ccalender&profile_id=3545430206020164202&title=HTTP/3"
    
    # Define the headers as provided
    headers = {
        "Host": "tenor.googleapis.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://tenor.com/",
        "Authorization": "Bearer ya29.a0AcM612zNr8gDfflDhHhTZE0YNX5iimopWtVt30yDDn9c13oPxjPb9BB8nowLvsj5r7kjkuocyB29h__UPNkQNEtFznxslzj_jdL4ajsjbDHbEZhcUYd7Oq4PgLAeMybCq6wvzqeeZCHwoOS9FKwQIjIRvUBo8r1ehRMaCgYKAcsSARISFQHGX2MisAbz53mB0-8jg7RLxBvDZw0170",
        "Content-Type": "image/gif",  
        "Origin": "https://tenor.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=0",
        "TE": "trailers"
    }

    # Path to the GIF file to upload (replace with the actual file path)
    file_path = os.path.abspath(os.path.join('..','video_to_gif', 'app', 'static', 'results', gif_location))

    
    # Read the GIF file as binary data
    with open(file_path, 'rb') as gif_file:
        gif_data = gif_file.read()
    
    # Make the POST request
    response = requests.post(url, headers=headers, data=gif_data)

    # Check the response
    if response.status_code == 200:
        print('GIF uploaded successfully')
        print('Response:', response.json())
    else:
        print("Failed to upload GIF")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
