import os
import shutil
import uuid
from fastapi import UploadFile
from moviepy.editor import VideoFileClip
import asyncio
from PIL import ImageDraw, ImageFont, ImageSequence, Image

# Function to resize video and convert it to GIF using moviepy
def convert_video_to_gif(video_path: str, gif_path: str):
    # Load the video
    clip = VideoFileClip(video_path)
    
    # Resize the video to 360p and reduce fps to 5 for GIF
    resized_clip = clip.resize(height=144).set_fps(5)
    
    # Save the resized video as GIF
    resized_clip.write_gif(gif_path)

def hex_to_rgb(hex_color):
    # Remove the hash symbol if it's there
    hex_color = hex_color.lstrip('#')
    # Convert hex to RGB tuple
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

async def process_video_upload_with_caption(upload_video: UploadFile, captions, font_size, boldness, font_color_one, font_color_two, outline_color, shadow_color, shadow_offset= '4,4', line_spacing = 10, font= 'Oswald.ttf'):
    print('with caption')

    try:
        # Convert necessary fields to integers
        font_size = int(font_size)
        boldness = int(boldness)
        
        # Ensure shadow_offset is a tuple of integers
        shadow_offset_values = shadow_offset.strip('()').split(',')

        if len(shadow_offset_values) != 2:
            raise ValueError("shadow_offset must contain exactly two values.")
            
        shadow_offset = tuple(map(int, shadow_offset_values))  # Convert to a tuple of integers

                
        shadow_offset = tuple(map(int, shadow_offset_values))  # Convert to a tuple of integers
        line_spacing = int(line_spacing)

        # Convert hex color values to RGB tuples
        font_color_one = hex_to_rgb(font_color_one)
        font_color_two = hex_to_rgb(font_color_two)
        outline_color = hex_to_rgb(outline_color)
        shadow_color = hex_to_rgb(shadow_color)

        # Ensure the 'uploads' and 'result' folders exist
        uploads_dir = os.path.abspath("app/static/uploads")
        result_dir = os.path.abspath("app/static/results")
        
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

        # Check if the font file exists
        font_path = os.path.join(os.path.abspath('app/fonts'), font)
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found at {font_path}")

        print("font path:", font_path)

        # Add text to the GIF
        await asyncio.to_thread(add_text_to_gif, gif_location, gif_location, captions, font_path, font_size, shadow_offset, shadow_color, outline_color, font_color_one, font_color_two, line_spacing, boldness)

        await upload_video.close()

        return {"status": "success", "gif_location": gif_filename, "message": upload_video.filename}
    except FileNotFoundError as fnf_error:
        print(f"Font file error: {fnf_error}")
        return {"status": "error", "message": f"Font file error: {str(fnf_error)}"}
    except ValueError as value_error:
        print(f"Value error: {value_error}")
        return {"status": "error", "message": f"Value error: {str(value_error)}"}
    except Exception as e:
        print(f"Error processing video with caption: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}







# Async function to process video upload without caption
async def process_video_upload(upload_video: UploadFile):
    try:
        # Ensure the 'uploads' and 'result' folders exist
        uploads_dir = os.path.abspath("app/static/uploads")
        result_dir = os.path.abspath("app/static/results")
        
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(result_dir, exist_ok=True)

        # Generate unique filenames for the video and GIF
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

# Function to add text to GIF frames
def add_text_to_gif(input_gif_path, output_gif_path, text, font_path, font_size=50, shadow_offset=(4, 4), shadow_color=(0, 0, 0, 128), outline_color=(0, 0, 0, 128), font_color1=(255, 255, 255, 255), font_color2=(204, 204, 255, 255), line_spacing=10, boldness=2):
    font = ImageFont.truetype(font_path, font_size)
    original_gif = Image.open(input_gif_path)
    frames = []

    max_width = original_gif.size[0] - 20
    lines = wrap_text(text, font, max_width)

    for frame_index, frame in enumerate(ImageSequence.Iterator(original_gif)):
        frame = frame.convert("RGBA")
        draw = ImageDraw.Draw(frame)

        frame_width = frame.size[0]
        frame_height = frame.size[1]

        total_text_height = sum([draw.textbbox((0, 0), line, font=font)[
                                3] for line in lines]) + (len(lines) - 1) * line_spacing

        y = frame_height - total_text_height - 10
        current_font_color = font_color1 if frame_index % 10 < 5 else font_color2

        for line in lines:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = (frame_width - text_width) // 2

            draw.text(
                (text_x + shadow_offset[0], y + shadow_offset[1]), line, font=font, fill=shadow_color)

            for x_offset in [-boldness, 0, boldness]:
                for y_offset in [-boldness, 0, boldness]:
                    if x_offset != 0 or y_offset != 0:
                        draw.text((text_x + x_offset, y + y_offset),
                                  line, font=font, fill=outline_color)

            draw.text((text_x, y), line, font=font, fill=current_font_color)
            y += text_height + line_spacing

        frames.append(frame)

    duration = original_gif.info.get('duration', 100)

    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )

    print(f"GIF with text saved at {output_gif_path}")

# Function to wrap text based on max width
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()

    while words:
        line = ''
        while words:
            test_line = line + words[0] + ' '
            # Ensure the width is compared as integers
            text_width = font.getbbox(test_line)[2]
            if isinstance(text_width, str):
                text_width = int(text_width)  # Convert to int if necessary

            if text_width <= max_width:
                line = test_line
                words.pop(0)
            else:
                break
        lines.append(line.strip())

    return lines





