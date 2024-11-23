import streamlit as st


def main() -> None:
    """Handles routing and page rendering."""
    st.set_page_config(layout="wide")
    pages = {
        "Editorial Tools": [
            st.Page("pages/get_news.py", title="Get News"),
            st.Page("pages/write_article.py", title="Generate an Article"),
        ],
        "Social Media Automation": [
            st.Page("pages/create_tiktok.py", title="Create a TikTok"),
            st.Page("pages/post_to_telegram.py", title="Create a Telegram Post"),
        ],
    }
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
