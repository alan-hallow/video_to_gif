import os
import shutil
import uuid
from fastapi import UploadFile
from moviepy.editor import VideoFileClip
import yt_dlp

def download_video_from_YT_link(url: str, output_path='static/uploads'):
    try:
        # Define options for yt-dlp
        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Use video title as file name
        }

        # Download the video and retrieve its info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract information and download video
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', None)  # Get the video title
            video_ext = info.get('ext', None)  # Get the video extension

            if video_title and video_ext:
                # Construct the full path to the downloaded video file
                video_filename = f"{video_title}.{video_ext}"
                return os.path.join(output_path, video_filename)
            else:
                raise FileNotFoundError("Video title or extension not found in metadata.")

    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return None
def convert_video_to_gif(video_path: str, gif_path: str):
    try:
        clip = VideoFileClip(video_path)
        resized_clip = clip.resize(height=360)
        resized_clip.write_gif(gif_path)
    except Exception as e:
        print(f"An error occurred during GIF conversion: {e}")

async def process_youtube_video(video_link: str):
    try:
        # Ensure directories exist
        uploads_dir = os.path.abspath("static/uploads")
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        results_dir = os.path.abspath("static/results")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Download the YouTube video
        video_path = download_video_from_YT_link(video_link, uploads_dir)
        if not video_path:
            return {"status": "error", "message": "Failed to download video from YouTube."}

        # Generate unique GIF filename
        unique_id = str(uuid.uuid4())
        gif_filename = f"{unique_id}.gif"
        gif_path = os.path.join(results_dir, gif_filename)

        # Convert the video to GIF
        convert_video_to_gif(video_path, gif_path)


        # Return the URL of the GIF
        gif_url = f"/static/results/{gif_filename}"
        return {"status": "success", "gif_url_youtube": gif_url, "message": "Video converted to GIF successfully!"}
    except Exception as e:
        print(f"Error processing video: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
