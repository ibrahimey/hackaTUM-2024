import os
import streamlit as st

from dotenv import load_dotenv

from modules.generator import generate_video
from utils.azure_client import AzureOpenAIClient

load_dotenv()

gpt = AzureOpenAIClient(
    endpoint=os.getenv("AZURE_OPENAI_GPT_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)
dalle = AzureOpenAIClient(
    endpoint=os.getenv("AZURE_OPENAI_DALLE_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

def create_video_page():
    st.title("Create Video From Article")
    st.write("Input an article below and click the button to generate a video.")

    # Input field for the article
    articles = [f for f in os.listdir("data/articles") if f.endswith(".txt")]
    if not articles:
        st.warning("No articles found. Please generate articles first.")
    else:
        selected_article = st.selectbox("Select an article to post:", ["Select an article"] + articles)

        if selected_article != "Select an article":
            article_path = os.path.join("data/articles", selected_article)
            with open(article_path, 'r') as file:
                article_content = file.read()

            st.text_area("Article Content:", article_content, height=200)

    # Button to create video
    if st.button("Create Video"):
        if article_content.strip():
            try:
                # Call the create_video function with the provided article text
                video_path = generate_video(article_content, llm=gpt, dalle=dalle)

                # Display success message
                st.success("Video created successfully!")

                # Display the video
                st.subheader("Generated Video")
                st.video(video_path)
            except Exception as e:
                st.error(f"An error occurred while creating the video: {e}")
        else:
            st.warning("Please enter an article before generating a video.")


create_video_page()

