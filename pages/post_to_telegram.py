import streamlit as st
import os
from utils.telegram_utils import telegram_sendMessage, telegram_sendVideo

# Constants
CHAT_ID = "@Lobsterinna"  # Replace with your channel name or chat ID
ARTICLE_DIR = "data/articles"  # Replace with your articles directory
VIDEO_DIR = "data/export"      # Replace with your videos directory


def post_to_telegram():
    st.title("Post to Telegram")

    # Dropdown options
    options = ["Select an option", "Post an Article", "Post a Video"]
    selection = st.selectbox("Choose what to post:", options)

    if selection == "Post an Article":
        if not os.path.exists(ARTICLE_DIR):
            st.error("Article directory does not exist.")
            return

        # Get list of articles
        articles = [f for f in os.listdir(ARTICLE_DIR) if f.endswith(".txt")]
        if not articles:
            st.warning("No articles found. Please generate articles first.")
        else:
            selected_article = st.selectbox("Select an article to post:", ["Select an article"] + articles)

            if selected_article != "Select an article":
                article_path = os.path.join(ARTICLE_DIR, selected_article)
                with open(article_path, 'r') as file:
                    article_content = file.read()

                st.text_area("Article Content:", article_content, height=200)

                if st.button("Post Article"):
                    response = telegram_sendMessage(text=article_content, chat_id=CHAT_ID)
                    st.success(f"Article posted successfully!")

    elif selection == "Post a Video":
        if not os.path.exists(VIDEO_DIR):
            st.error("Video directory does not exist.")
            return

        # Get list of videos
        videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".mkv"))]
        if not videos:
            st.warning("No videos found. Please generate videos first.")
        else:
            selected_video = st.selectbox("Select a video to post:", ["Select a video"] + videos)

            if selected_video != "Select a video":
                video_path = os.path.join(VIDEO_DIR, selected_video)
                st.video(video_path)
                caption = st.text_input("Enter a caption for the video:")

                if st.button("Post Video"):
                    response = telegram_sendVideo(video_path=video_path, chat_id=CHAT_ID, caption=caption)
                    st.success(f"Video posted successfully!")


post_to_telegram()
