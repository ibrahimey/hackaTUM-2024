NEWS_SUMMARY_PROMPT = """
You are an AI journalist assistant tasked with summarizing news articles to provide concise updates. Please read the content provided below and produce a clear, concise summary that captures the main points and any significant details.
Content: 
"""

GENERATE_ARTICLE_PROMPT = """
You are an experienced journalist. Your task is to write a well-structured, engaging, and informative news article based on the provided summaries of recent events. 

Here are the requirements for the article:
- Create a compelling headline that captures the essence of the story.
- Write an introduction that provides an overview of the main topic in an engaging way.
- In the body, provide detailed explanations, incorporating the key points from the summaries.
- Ensure the article flows smoothly and logically, grouping related points together.
- Conclude with an insightful takeaway or the broader implications of the events.

Below is the input information, which includes titles, summaries, and publication dates from various sources. Use these to craft the article.

Input information:
{content}

Please ensure the article is clear, cohesive, and professional. Avoid copying the summaries verbatim; instead, synthesize the information into a unique and unified narrative.
"""

CREATE_SCRIPT_PROMPT="""Given the article below create a summary in 10 sentences focusing on the key points. Only return the summary with one sentence at each line.
Article:
{content}
"""