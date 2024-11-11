import os
import uuid
from moviepy.editor import VideoFileClip
import yt_dlp

def download_YT_channel_Specific_Number_videos(channel_url: str, output_path='static/uploads', max_videos=2):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    try:
        downloaded_paths = []
        
        # Define yt-dlp options to retrieve channel videos
        ydl_opts = {
            'format': 'worstvideo',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Use video title as filename
            'playlistend': max_videos,  # Limit to the first `max_videos` videos
            'noplaylist': False,        # Enable playlist mode to get multiple videos
        }

        # Download videos from the channel and retrieve information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            channel_info = ydl.extract_info(channel_url, download=True)  # Extract channel info
            downloaded_videos = channel_info.get('entries', [])  # Get the list of videos

            for index, video in enumerate(downloaded_videos[:max_videos], start=1):
                # Construct the filename with formatted index
                video_ext = video.get('ext', 'mp4')
                video_filename = f"{index:04d}.{video_ext}"
                full_path = os.path.join(output_path, video_filename)

                # Rename the downloaded file to the formatted filename
                original_path = os.path.join(output_path, f"{video['title']}.{video_ext}")
                if os.path.exists(original_path):
                    os.rename(original_path, full_path)
                    downloaded_paths.append(full_path)
                    print(f"Downloaded and renamed: {full_path}")
                else:
                    print(f"File not found for renaming: {original_path}")

        print(f"Download of up to {max_videos} videos completed!")
        return downloaded_paths  # Return the list of downloaded video paths

    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return None


def convert_video_to_gif(video_path: str, gif_path: str):
    try:
        clip = VideoFileClip(video_path)
        resized_clip = clip.resize(height=360)
        resized_clip.write_gif(gif_path)
        print(f"Converted {video_path} to GIF at {gif_path}")
    except Exception as e:
        print(f"An error occurred during GIF conversion: {e}")

async def process_youtube_channel(video_link: str):
    try:
        # Ensure directories exist
        uploads_dir = os.path.abspath("app/static/uploads")
        results_dir = os.path.abspath("app/static/results")
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        # Download the YouTube videos
        video_paths = download_YT_channel_Specific_Number_videos(video_link, uploads_dir, max_videos=2)
        if not video_paths:
            return {"status": "error", "message": "Failed to download video from YouTube."}

        gif_urls = []  # Store GIF filenames
        for video_path in video_paths:
            # Generate unique GIF filename
            unique_id = str(uuid.uuid4())
            gif_filename = f"{unique_id}.gif"
            gif_path = os.path.join(results_dir, gif_filename)

            # Convert the video to GIF
            convert_video_to_gif(video_path, gif_path)

            # Add to the list of GIF URLs
            gif_urls.append(gif_filename)

        return {"status": "success", "gif_urls": gif_urls, "message": "Videos converted to GIFs successfully!"}
    except Exception as e:
        print(f"Error processing video: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
