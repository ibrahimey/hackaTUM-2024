from moviepy.editor import *
import os
from gtts import gTTS
from PIL import Image

from .prompts import CREATE_SCRIPT_PROMPT
from utils.azure_client import AzureOpenAIClient

def create_script(article, llm: AzureOpenAIClient):
    script = llm(CREATE_SCRIPT_PROMPT.format(content=article)).split('\n')
    return script

def create_tiktok(script, images, output_path="data/export/video.mp4"):
    os.makedirs("data/audio", exist_ok=True)
    for i, text in enumerate(script):
        tts = gTTS(text=text, lang='en')
        tts.save(f"data/audio/voiceover{i}.mp3")

    os.makedirs("data/processed_images", exist_ok=True)
    target_resolution = (720, 1280)  # Mobile-friendly vertical resolution

    # TODO: use image urls
    for image_file in os.listdir("data/images"):
        img = Image.open(f"data/images/{image_file}")
        img_ratio = img.width / img.height
        target_ratio = target_resolution[0] / target_resolution[1]

        # Resize while maintaining aspect ratio
        if img_ratio > target_ratio:
            # Wider image: fit width, crop height
            new_width = target_resolution[0]
            new_height = int(target_resolution[0] / img_ratio)
        else:
            # Taller image: fit height, crop width
            new_width = int(target_resolution[1] * img_ratio)
            new_height = target_resolution[1]

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a blank image (black background) with target resolution
        final_img = Image.new("RGB", target_resolution, (0, 0, 0))
        # Paste resized image centered on the blank image
        paste_x = (target_resolution[0] - new_width) // 2
        paste_y = (target_resolution[1] - new_height) // 2
        final_img.paste(resized_img, (paste_x, paste_y))

        # Save the processed image
        final_img.save(f"data/processed_images/{image_file}")

    audio_clips = []
    image_clips = []
    length = -0.5

    start_times = [0]

    for audio_file in sorted(os.listdir("data/audio")):
        audio_clip = AudioFileClip(f"data/audio/{audio_file}")
        audio_clips.append(audio_clip.set_start(length + 0.5))
        length += audio_clip.duration + 0.5
        start_times.append(length)

    for i, image_file in enumerate(sorted(os.listdir("data/processed_images"))):
        clip = ImageClip(f"data/processed_images/{image_file}", duration=audio_clips[i].duration).set_start(start_times[i])
        image_clips.append(clip)

    videoImages = CompositeVideoClip(image_clips)
    videoAudio = CompositeAudioClip(audio_clips)

    videoImages.audio = videoAudio

    os.makedirs("data/export", exist_ok=True)
    videoImages.write_videofile(output_path, fps=1)
