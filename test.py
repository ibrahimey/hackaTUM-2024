from utils.azure_client import AzureOpenAIClient
from utils.json_utils import read_json_file
from utils.modules import get_news, summarize_news

# get_news(
#     source_url="https://rss.app/feeds/u6rcvfy6PTSf9vQ4.xml",
#     output_file_path="./data/news.json",
# )
llm = AzureOpenAIClient(
    temperature=0.6, top_p=0.95
)
news_list = read_json_file("data/news.json")
summaries = summarize_news(news_list, llm)
print(summaries)