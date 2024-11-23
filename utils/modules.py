import feedparser

from .json_utils import write_json_file


def get_news(source="https://rss.app/feeds/u6rcvfy6PTSf9vQ4.xml", destination="./data/news.json"):
    """

    :param source: RSS feed to get the news
    :param destination: Where to save the feed
    :return:
    """
    feed = feedparser.parse(source)

    if feed.status == 200:
        write_json_file(destination, feed.entries)
    else:
        print("Failed to get RSS feed. Status code: ", feed.status)
