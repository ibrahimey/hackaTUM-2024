import os

from dotenv import load_dotenv

from modules.article_writer import generate_article
from modules.news_summarizer import summarize_news
from modules.rss_feed_parser import get_news
from modules.filter_EV_articles import filter_ev_articles
from utils.azure_client import AzureOpenAIClient
from utils.json_utils import read_json_file
from modules.image_generator import generate_article_images


load_dotenv()

gpt = AzureOpenAIClient(endpoint=os.getenv("AZURE_OPENAI_GPT_ENDPOINT"), api_key=os.getenv("AZURE_OPENAI_API_KEY"))
dalle = AzureOpenAIClient(endpoint=os.getenv("AZURE_OPENAI_DALLE_ENDPOINT"), api_key=os.getenv("AZURE_OPENAI_API_KEY"))

# Parse sources
# get_news(
#     source_url="https://rss.app/feeds/u6rcvfy6PTSf9vQ4.xml",
#     output_file_path="./data/news.json",
# )

# Discover topics
# news_list = read_json_file("data/news.json")
# summaries = summarize_news(news_list, gpt)

# Write article
relevant_articles = filter_ev_articles(read_json_file("data/news.json"), gpt)
# print(len(relevant_articles))

article = generate_article(relevant_articles, gpt)
print(article)

# Generate image
# image = generate_article_images(article, dalle)
# print(image)
# with open('output_image.png', 'wb') as file:
#     file.write(image)
