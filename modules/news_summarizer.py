import feedparser
import requests

from bs4 import BeautifulSoup
from pathlib import Path
from typing import Union

from .prompts import FILTER_PROMPT, SUMMARIZE_NEWS_PROMPT

from utils.azure_client import AzureOpenAIClient
from utils.json_utils import write_json_file


def get_news(source_url: str, output_file_path: Union[str, Path]):
    """
    Fetches news from a specified RSS feed URL and saves the entries to a destination file.

    :param source_url: RSS feed URL to get the news
    :param output_file_path: Path to save the retrieved feed entries
    """
    feed = feedparser.parse(source_url)
    if feed.status == 200:
        news_list = []
        titles = {}
        links = {}
        for entry in feed.entries:
            if entry["title"] in titles or entry["link"] in links:
                continue
            titles[entry["title"]] = True
            links[entry["link"]] = True
            news_list.append(entry)
        return news_list
    else:
        print(f"Failed to get RSS feed. Status code: {feed.status}", feed.status)


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


def filter_ev_articles(relevant_articles, category, llm: AzureOpenAIClient):
    """
    Filters articles to keep only those relevant to electric vehicles.
    """
    filtered_articles = []

    for article in relevant_articles:
        # Format the input for the prompt
        if "generated_summary" not in article:
            continue
        content = (
            f"\nTitle: {article['title']}\nSummary: {article['generated_summary']}\n"
        )
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": FILTER_PROMPT.format(category=category),
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            "temperature": 0.4,
            "top_p": 0.95,
        }
        # Use the language model to assess relevance
        response = llm.send_request(payload)

        # Parse the response to check if it's '1' (relevant)
        if response == "1":
            filtered_articles.append(article)

    return filtered_articles
