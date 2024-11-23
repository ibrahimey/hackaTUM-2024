import feedparser

from pathlib import Path
from typing import Union

from utils.json_utils import write_json_file


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
        print(f"Failed to get RSS feed. Status code: {feed.status}", feed.status)
