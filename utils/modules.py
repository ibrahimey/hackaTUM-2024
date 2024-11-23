import feedparser
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from typing import Union

from .azure_client import AzureOpenAIClient
from .json_utils import write_json_file
from .prompts import NEWS_SUMMARY_PROMPT, NEW_ARTICLE_PROMPT

load_dotenv()


def get_news(source_url: str, output_file_path: Union[str, Path]):
    """
    Fetches news from a specified RSS feed URL and saves the entries to a destination file.

    :param source_url: RSS feed URL to get the news
    :param output_file_path: Path to save the retrieved feed entries
    """
    feed = feedparser.parse(source_url)
    if feed.status == 200:
        write_json_file(output_file_path, feed.entries)
    else:
        print("Failed to get RSS feed. Status code: ", feed.status)  # TODO: return an error


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
        print("Failed to retrieve content. Status code: ", response.status_code)  # TODO: return an error


def summarize_news(news_list: list, llm: AzureOpenAIClient):
    summarized_news = []
    for i, news in enumerate(news_list):
        try:
            text = fetch_webpage_content(news["link"])
            summary = llm(NEWS_SUMMARY_PROMPT + text)
            summarized_news.append(summary)
            news_list[i]["generated_summary"] = summary
        except Exception as e:
            print(f"Error summarizing news item {i + 1}: {e}")  # TODO: return an error
    write_json_file("./data/news.json", news_list)
    return summarized_news


def write_article(summarized_news: list, llm: AzureOpenAIClient):
    """
    Given the summaries of various news items about a topic, generates a new article about that topic
    :param summarized_news: list of strings
    :param llm: LLM to use to generate the article
    :return: string containing the article text
    """
    combined_news = "\n\n".join(summarized_news)
    article = llm(NEW_ARTICLE_PROMPT + combined_news)

    return article
