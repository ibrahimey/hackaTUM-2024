import os
import streamlit as st

from dotenv import load_dotenv

from modules.article_writer import generate_article
from modules.image_generator import generate_article_images
from utils.azure_client import AzureOpenAIClient
from utils.json_utils import read_json_file

load_dotenv()

gpt = AzureOpenAIClient(
    endpoint=os.getenv("AZURE_OPENAI_GPT_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)
dalle = AzureOpenAIClient(
    endpoint=os.getenv("AZURE_OPENAI_DALLE_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


def generate_article_page():
    st.title("Generate a New Article")
    st.write("Select articles to generate a new article.")

    # Load articles from news.json
    news_file = "./data/news.json"  # Adjust the path if needed
    articles = read_json_file(news_file)

    if not articles:
        st.warning("No articles found. Please fetch news first.")
        return

    # Dropdown menu for selecting articles
    selected_articles = st.multiselect(
        "Select articles",
        options=[article["title"] for article in articles],
        default=[],
    )

    if st.button("Generate Article"):
        if selected_articles:
            # Find the full articles corresponding to the selected titles
            selected_content = [
                article for article in articles if article["title"] in selected_articles
            ]
            try:
                # Call write_article with selected articles
                generated_article = generate_article(selected_content, gpt)
                st.subheader("Generated Article")
                try:
                    image_data = generate_article_images(generated_article, dalle)
                    st.image(image_data, width=300)
                except Exception:
                    print("error")
                st.write(generated_article)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please select at least one article to generate an article.")


generate_article_page()
