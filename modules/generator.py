import nltk
import os
import requests
import time

from datetime import datetime
from gtts import gTTS
from moviepy.editor import *
from nltk.tokenize import sent_tokenize
from PIL import Image

from .prompts import (
    CREATE_SCRIPT_PROMPT,
    GENERATE_ARTICLE_IMAGE_PROMPT,
    GENERATE_ARTICLE_PROMPT,
)

from utils.azure_client import AzureOpenAIClient

nltk.download("punkt_tab")


def generate_article(relevant_articles: list, llm: AzureOpenAIClient):
    combined_content = "\n".join(
        [
            f"Title: {article['title']}\nSummary: {article.get('generated_summary', article['summary'])}"
            for article in relevant_articles
        ]
    )
    return llm.send_text_generation_request(
        GENERATE_ARTICLE_PROMPT.format(content=combined_content)
    )


def generate_article_image(article: str, llm: AzureOpenAIClient):
    return llm.generate_image(GENERATE_ARTICLE_IMAGE_PROMPT.format(article=article))


def create_script(article, llm: AzureOpenAIClient):
    return sent_tokenize(
        llm.send_text_generation_request(CREATE_SCRIPT_PROMPT.format(content=article))
    )


def generate_tiktok_image(article: str, llm: AzureOpenAIClient):
    return llm.generate_image(
        GENERATE_ARTICLE_IMAGE_PROMPT.format(article=article), size="1024x1792"
    )


def generate_images(article: str, llm: AzureOpenAIClient):
    urls = []
    for i in range(3):
        try:
            url = generate_tiktok_image(article, llm)
        except Exception as e:
            url = i
        urls.append(url)
        time.sleep(5)

    return urls


def generate_video(
    article: str,
    llm: AzureOpenAIClient,
    dalle: AzureOpenAIClient,
    output_path=f"data/export/video{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4",
):
    script = create_script(article=article, llm=llm)

    # Generate audio files for each text in the script
    os.makedirs("data/audio", exist_ok=True)
    for i, text in enumerate(script):
        tts = gTTS(text=text, lang="en")
        tts.save(f"data/audio/voiceover{i}.mp3")

    # Process images to a mobile-friendly resolution
    os.makedirs("data/processed_images", exist_ok=True)
    target_resolution = (720, 1280)  # Mobile-friendly vertical resolution

    for i, image_url in enumerate(generate_images(script, dalle)):
        if image_url in range(3):
            img = Image.open(f"data/backup_images/{image_url}.jpeg")
        else:
            img = Image.open(requests.get(image_url, stream=True).raw)
        img_ratio = img.width / img.height
        target_ratio = target_resolution[0] / target_resolution[1]

        # Resize while maintaining aspect ratio
        if img_ratio > target_ratio:
            new_width = target_resolution[0]
            new_height = int(target_resolution[0] / img_ratio)
        else:
            new_width = int(target_resolution[1] * img_ratio)
            new_height = target_resolution[1]

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a blank image (black background) with target resolution
        final_img = Image.new("RGB", target_resolution, (0, 0, 0))
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
        # Create an ImageClip
        image_clip = ImageClip(
            f"data/processed_images/{image}", duration=audio_clips[i].duration
        ).set_start(start_times[i])
        image_clips.append(image_clip)

    # Combine all image clips
    video_images = CompositeVideoClip(image_clips)
    video_audio = CompositeAudioClip(audio_clips)

    # Add audio to the video
    video_images.audio = video_audio

    # Export the video
    os.makedirs("data/export", exist_ok=True)
    video_images.write_videofile(output_path, fps=2)

    return output_path
