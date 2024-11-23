from .prompts import GENERATE_ARTICLE_PROMPT

from utils.azure_client import AzureOpenAIClient


def generate_article(relevant_articles: list, llm: AzureOpenAIClient):
    combined_content = "\n".join(
        [
            f"Title: {article['title']}\nSummary: {article['generated_summary']}"
            for article in relevant_articles
        ]
    )
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": GENERATE_ARTICLE_PROMPT.format(
                            content=combined_content
                        ),
                    },
                ],
            },
        ],
        "temperature": 0.4,
        "top_p": 0.95,
    }
    return llm.send_request(payload)
