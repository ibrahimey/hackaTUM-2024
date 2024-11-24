import streamlit as st

from modules.news_summarizer import get_news
from utils.json_utils import read_json_file

from html import unescape


def display_news(news_list):
    for news in news_list:
        with st.container():
            st.subheader(news["title"])
            st.write(unescape(news["generated_summary"]))
            if news["media_content"]:
                st.image(news["media_content"][0]["url"], width=300)
            st.write(f"Published by {news['author']} on {news['published']}")
            st.markdown(f"[Read more]({news['link']})", unsafe_allow_html=True)
            st.divider()


def get_news_page():
    st.title("RSS Feed Reader")
    st.write("Enter an RSS feed URL below to fetch the latest news.")

    # Input field for RSS feed URL
    rss_url = st.text_input("RSS Feed URL", placeholder="Enter a valid RSS feed URL")

    # Button to fetch news
    if st.button("Get News"):
        if rss_url.strip():
            output_file = "./data/news.json"
            try:
                # Call the get_news function with the provided URL and output file
                get_news(rss_url, output_file)

                # Read the news items from the file
                news_items = read_json_file(output_file)
                if news_items:
                    st.success(f"Fetched {len(news_items)} news items!")
                    for news in news_items:
                        st.write(news["title"])
                        st.write(news["link"])
                        st.write("---")
                else:
                    st.warning("No news items found in the file.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid RSS feed URL.")

    display_news(read_json_file("./data/news.json"))


get_news_page()
