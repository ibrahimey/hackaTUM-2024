from moviepy.editor import *
import os
import time
from datetime import datetime
import requests
from gtts import gTTS
from PIL import Image
import nltk
from nltk.tokenize import sent_tokenize

from .prompts import CREATE_SCRIPT_PROMPT, GENERATE_ARTICLE_IMAGE_PROMPT
from utils.azure_client import AzureOpenAIClient

nltk.download('punkt_tab')

def generate_tiktok_image(article: str, llm: AzureOpenAIClient):
    payload = {
        "prompt": GENERATE_ARTICLE_IMAGE_PROMPT.format(article=article),
        "n": 1,
        "size": "1024x1792",
    }
    return llm.send_request(payload)

def generate_images(article, llm):
    urls = []
    for i in range(3):
        url = generate_tiktok_image(article, llm)
        urls.append(url)
        time.sleep(10)

    return urls

def create_script(article, llm: AzureOpenAIClient):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": CREATE_SCRIPT_PROMPT.format(content=article),
                    },
                ],
            },
        ],
        "temperature": 0.4,
        "top_p": 0.95,
    }
    script = sent_tokenize(llm.send_request(payload))
    return script

def create_tiktok(article, llm, dalle, output_path=f"data/export/video{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"):
    script = create_script(article=article, llm=llm)

    os.makedirs("data/audio", exist_ok=True)
    for i, text in enumerate(script):
        tts = gTTS(text=text, lang='en')
        tts.save(f"data/audio/voiceover{i}.mp3")

    os.makedirs("data/processed_images", exist_ok=True)
    target_resolution = (720, 1280)  # Mobile-friendly vertical resolution

    for i, image_url in enumerate(generate_images(script, dalle)):
        img = Image.open(requests.get(image_url, stream=True).raw)
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
        final_img.save(f"data/processed_images/{i}.png")

    audio_clips = []
    image_clips = []
    length = -0.5

    start_times = [0]

    for audio_file in sorted(os.listdir("data/audio")):
        audio_clip = AudioFileClip(f"data/audio/{audio_file}")
        audio_clips.append(audio_clip.set_start(length + 0.5))
        length += audio_clip.duration + 0.5
        start_times.append(length)

    for i, image in enumerate(sorted(os.listdir("data/processed_images"))):
        clip = ImageClip(f"data/processed_images/{image}", duration=audio_clips[i].duration).set_start(start_times[i])
        image_clips.append(clip)

    videoImages = CompositeVideoClip(image_clips)
    videoAudio = CompositeAudioClip(audio_clips)

    videoImages.audio = videoAudio

    os.makedirs("data/export", exist_ok=True)
    videoImages.write_videofile(output_path, fps=1)

    return output_path
