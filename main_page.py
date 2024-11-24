import streamlit as st


def main() -> None:
    st.logo("logo.jpeg", size="large")
    st.set_page_config(layout="wide")
    st.markdown(
        """
            <style>
            .st-emotion-cache-1jicfl2 {
                padding-top: 3rem;
            }
            </style>
            """,
        unsafe_allow_html=True,
    )
    pages = {
        "Daily Highlights": [
            st.Page("pages/ev_news_today.py", title="EV Article of the Day", icon="⚡"),
        ],
        "Editorial Tools": [
            st.Page("pages/get_news.py", title="Get News", icon="📰"),
            st.Page("pages/write_article.py", title="Generate an Article", icon="💡"),
        ],
        "Social Media Automation": [
            st.Page("pages/create_tiktok.py", title="Create a TikTok", icon="🎥"),
            st.Page(
                "pages/post_to_telegram.py", title="Create a Telegram Post", icon="📱"
            ),
        ],
    }
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
