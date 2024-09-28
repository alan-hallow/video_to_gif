import os
import shutil
import uuid
from fastapi import UploadFile
from moviepy.editor import VideoFileClip
import asyncio

# Function to resize video and convert it to GIF using moviepy
def convert_video_to_gif(video_path: str, gif_path: str):
    # Load the video
    clip = VideoFileClip(video_path)
    
    # Resize the video to 360p
    resized_clip = clip.resize(height=360)

    resized_clip = resized_clip.set_fps(5)

    
    # Save the resized video as GIF
    resized_clip.write_gif(gif_path)

async def process_video_upload(upload_video: UploadFile):
    try:
        # Ensure the 'uploads' and 'result' folders exist
        uploads_dir = os.path.abspath("static/uploads")
        result_dir = os.path.abspath("static/results")
        
        for directory in [uploads_dir, result_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        unique_video_filename = f"{uuid.uuid4()}_{upload_video.filename}"
        video_location = os.path.join(uploads_dir, unique_video_filename)
        gif_filename = f"{uuid.uuid4()}.gif"
        gif_location = os.path.join(result_dir, gif_filename)

        # Save the uploaded video file asynchronously
        await asyncio.to_thread(save_upload_video, upload_video, video_location)

        # Convert video to GIF asynchronously
        await asyncio.to_thread(convert_video_to_gif, video_location, gif_location)

        await upload_video.close()

        return {"status": "success", "gif_location": gif_filename, "message": f"Video '{upload_video.filename}' converted to GIF successfully!"}
    except Exception as e:
        print(f"Error processing video: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

# Helper function to save the uploaded video
def save_upload_video(upload_video: UploadFile, video_location: str):
    with open(video_location, "wb+") as file_object:
        shutil.copyfileobj(upload_video.file, file_object)