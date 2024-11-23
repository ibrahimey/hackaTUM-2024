from .prompts import GENERATE_ARTICLE_IMAGE_PROMPT

from utils.azure_client import AzureOpenAIClient


def generate_article_images(article: str, llm: AzureOpenAIClient):
    payload = {
        "prompt": GENERATE_ARTICLE_IMAGE_PROMPT.format(article=article),
        "n": 1,
        "size": "1024x1024",
    }
    return llm.send_request(payload)
