import requests

from bs4 import BeautifulSoup

from .prompts import SUMMARIZE_NEWS_PROMPT

from utils.azure_client import AzureOpenAIClient
from utils.json_utils import write_json_file


def fetch_webpage_content(url: str):
    """
    Fetches and returns the main textual content from a specified webpage URL.

    :param url: The URL of the webpage to fetch content from.
    :return: A string containing the stripped text from the webpage if successful, None otherwise.
    """
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
    )
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join(soup.stripped_strings)
        return text
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")


def summarize_news(news_list: list, llm: AzureOpenAIClient):
    for i, news in enumerate(news_list):
        try:
            content = fetch_webpage_content(news["link"])
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": SUMMARIZE_NEWS_PROMPT.format(content=content),
                            },
                        ],
                    },
                ],
                "temperature": 0.4,
                "top_p": 0.95,
            }
            summary = llm.send_request(payload)
            news_list[i]["generated_summary"] = summary
        except Exception as e:
            print(f"Error summarizing news item {i + 1}: {e}")
    return news_list
