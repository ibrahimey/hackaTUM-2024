from modules.article_writer import generate_article
from modules.news_summarizer import summarize_news
from modules.rss_feed_parser import get_news
from utils.azure_client import AzureOpenAIClient
from utils.json_utils import read_json_file


llm = AzureOpenAIClient(temperature=0.6, top_p=0.95)

rss_feeds = []
# Parse sources
get_news(
    source_url="https://rss.app/feeds/u6rcvfy6PTSf9vQ4.xml",
    output_file_path="./data/news.json",
)

news_list = read_json_file("data/news.json")

# Discover topics
summaries = summarize_news(news_list, llm)

# Write article
# article = generate_article(relevant_articles, llm)

# Generate image
# image = generate_article_image(article, llm)
