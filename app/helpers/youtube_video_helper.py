import os
import uuid
from fastapi import UploadFile
from moviepy.editor import VideoFileClip
import yt_dlp


def download_video_from_YT_link(url: str, output_path='static/uploads') -> str:
    """
    Download a video from YouTube and return the file path with a random name.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Generate a random file name
        random_name = str(uuid.uuid4())
        
        # Define options for yt-dlp
        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': f'{output_path}/{random_name}.%(ext)s',  # Use random name for the file
        }

        # Download the video and retrieve its metadata
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_ext = info.get('ext', 'mp4')  # Get video extension or fallback

            # Construct the file path
            video_filename = f"{random_name}.{video_ext}"
            video_path = os.path.join(output_path, video_filename)

            # Ensure the file exists
            if os.path.exists(video_path):
                return video_path
            else:
                raise FileNotFoundError(f"Downloaded file not found: {video_path}")

    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return None


def convert_video_to_gif(video_path: str, gif_path: str):
    """
    Convert a video to a GIF.
    """
    try:
        # Resize video and save as GIF
        clip = VideoFileClip(video_path)
        resized_clip = clip.resize(height=144).set_fps(5)
    
        # Save the resized video as GIF
        resized_clip.write_gif(gif_path)
    except Exception as e:
        print(f"An error occurred during GIF conversion: {e}")


async def process_youtube_video(video_link: str) -> dict:
    """
    Process a YouTube video by downloading it and converting it to a GIF.
    """
    try:
        # Ensure directories exist
        uploads_dir = os.path.abspath("app/static/uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        results_dir = os.path.abspath("app/static/results")
        os.makedirs(results_dir, exist_ok=True)

        # Download the YouTube video
        video_path = download_video_from_YT_link(video_link, uploads_dir)
        if not video_path:
            return {"status": "error", "message": "Failed to download video from YouTube."}

        # Generate unique GIF filename
        unique_id = str(uuid.uuid4())
        gif_filename = f"{unique_id}.gif"
        gif_path = os.path.join(results_dir, gif_filename)

        # Convert the video to a GIF
        convert_video_to_gif(video_path, gif_path)

        # Return the GIF URL
        gif_url = f"/static/results/{gif_filename}"
        return {"status": "success", "gif_url_youtube": gif_url, "message": "Video converted to GIF successfully!"}

    except Exception as e:
        print(f"Error processing video: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
