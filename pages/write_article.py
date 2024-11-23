import streamlit as st
from utils.json_utils import read_json_file
from modules.article_writer import generate_article
from utils.azure_client import AzureOpenAIClient

llm = AzureOpenAIClient(temperature=0.6, top_p=0.95)

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
        options=[article['title'] for article in articles],
        default=[]
    )

    if st.button("Generate Article"):
        if selected_articles:
            # Find the full articles corresponding to the selected titles
            selected_content = [
                article for article in articles if article['title'] in selected_articles
            ]
            try:
                # Call write_article with selected articles
                generated_article = generate_article(selected_content, llm)
                st.subheader("Generated Article")
                st.write(generated_article)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please select at least one article to generate an article.")

# Run the page function
if __name__ == "__main__":
    generate_article_page()
