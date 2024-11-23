from prompts import GENERATE_ARTICLE_PROMPT

from utils.azure_client import AzureChatOpenAI


def generate_article(relevant_articles, llm: AzureChatOpenAI):
    combined_content = "\n".join(
        [
            f"Title: {article['title']}\nSummary: {article['generated_summary']}"
            for article in relevant_articles
        ]
    )
    return llm(GENERATE_ARTICLE_PROMPT.format(content=combined_content))
