import datetime

import streamlit as st


def ev_news_today_page():
    st.title("Electric Vehicles Article of the Day 🚗⚡💚")

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    file_path = f"./data/articles/daily/{date_string}.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    start = content.find("**") + 2
    end = content.find("**", start)
    title = content[start:end].strip()
    col1, col2 = st.columns([1, 0.5])
    st.header(title)
    paragraphs = [p for p in content.split("\n")]
    st.write(paragraphs[2])
    col1, col2 = st.columns([0.3, 1])
    with col2:
        st.write(paragraphs[4])
        st.write(paragraphs[6])
        st.write(paragraphs[8])
        st.write(paragraphs[10])
    with col1:
        st.video(f"./data/videos/daily/{date_string}.mp4")

    col1, col2 = st.columns([1, 0.5])
    with col1:
        st.write(paragraphs[12])
        st.write(paragraphs[14])
    with col2:
        st.image("/Users/q672276/Documents/hackaTUM-2024/data/images/2024-11-24.png", width=300)


ev_news_today_page()
