import os
import streamlit as st

from dotenv import load_dotenv

from modules.tiktok_creator import create_tiktok
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
    article_text = st.text_area(
        "Enter your article here",
        placeholder="Paste or write your article...",
        height=200
    )

    # Button to create video
    if st.button("Create Video"):
        if article_text.strip():
            try:
                # Call the create_video function with the provided article text
                video_path = create_tiktok(article_text, llm=gpt, dalle=dalle)

                # Display success message
                st.success("Video created successfully!")

                # Display the video
                st.subheader("Generated Video")
                st.video(video_path)
            except Exception as e:
                st.error(f"An error occurred while creating the video: {e}")
        else:
            st.warning("Please enter an article before generating a video.")


# Run the page function
if __name__ == "__main__":
    create_video_page()

