import os
import streamlit as st

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from modules.news_summarizer import get_news, summarize_news, filter_ev_articles
from utils.azure_client import AzureOpenAIClient
from utils.json_utils import read_json_file, write_json_file, append_json_file

from html import unescape

load_dotenv()

gpt = AzureOpenAIClient(
    endpoint=os.getenv("AZURE_OPENAI_GPT_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


def display_news(news_list):
    for news in news_list:
        with st.container():
            title_col, date_col = st.columns([1, 0.3], vertical_alignment="center")
            with title_col:
                st.subheader(news["title"])
            with date_col:
                st.write(news['published'])
            col1, col2 = st.columns([0.3, 1])
            with col1:
                if "media_content" in news:
                    st.image(news["media_content"][0]["url"], use_column_width=True)
                elif "summary" in news:
                    soup = BeautifulSoup(news['summary'], 'html.parser')
                    img_tag = soup.find('img')
                    st.image(img_tag['src'], use_column_width=True)
            with col2:
                if "generated_summary" in news:
                    st.write(unescape(news["generated_summary"]))
                else:
                    st.write(unescape(news["summary"]))
            st.markdown(f"[Read more]({news['link']})", unsafe_allow_html=True)
            st.divider()


def get_news_page():
    st.title("RSS Feed Reader")
    
    col1, col2 = st.columns([1, 1])
    
    with col2:
        categories = ["All", "Electric Vehicles", "Politics", "Football", "Other"]
        selected_articles = st.selectbox(
            "Select topics",
            options=[category for category in categories],
        )

    with col1:
        # Input field for RSS feed URL
        rss_url = st.text_input("Enter an RSS feed URL below to fetch the latest news", placeholder="Enter a valid RSS feed URL")

        # Button to fetch news
        if st.button("Get News"):
            if rss_url.strip():
                output_file = "./data/news.json"
                try:
                    # Call the get_news function with the provided URL and output file
                    news_list = get_news(rss_url, output_file)
                    write_json_file("./data/news.json", summarize_news(news_list, gpt))
                    filtered_news_list = filter_ev_articles(news_list, "Electric Vehicles", gpt)
                    write_json_file(f"./data/news/electric_vehicles.json", filtered_news_list)

                    # Read the news items from the file
                    news_items = read_json_file(output_file)
                    if news_items:
                        st.success(f"Fetched {len(news_items)} news items!")
                        # for news in news_items:
                        #     st.write(news["title"])
                        #     st.write(news["link"])
                        #     st.write("---")
                    else:
                        st.warning("No news items found in the file.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a valid RSS feed URL.")

    news_list = read_json_file("./data/news.json")
    if selected_articles and selected_articles != "All":
        if selected_articles == "Electric Vehicles":
            news_list = read_json_file("./data/news/electric_vehicles.json")
        else:
            news_list = filter_ev_articles(news_list, selected_articles, gpt)
    display_news(news_list)


get_news_page()
