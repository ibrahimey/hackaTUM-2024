from .prompts import FILTER_EV_PROMPT

from utils.azure_client import AzureOpenAIClient


def filter_ev_articles(relevant_articles, llm: AzureOpenAIClient):
    """
    Filters articles to keep only those relevant to electric vehicles.
    """
    filtered_articles = []

    for article in relevant_articles:
        # Format the input for the prompt
        content = f"\nTitle: {article['title']}\nSummary: {article['generated_summary']}\n"
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": FILTER_EV_PROMPT,
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            "temperature": 0.4,
            "top_p": 0.95,
        }
        # Use the language model to assess relevance
        response = llm.send_request(payload)

        # Parse the response to check if it's '1' (relevant)
        if response == "1":
            filtered_articles.append(article)

    return filtered_articles
