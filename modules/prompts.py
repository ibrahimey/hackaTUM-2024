SUMMARIZE_NEWS_PROMPT = """
You are an AI journalist assistant with expertise in creating professional, concise, and engaging summaries of news articles. Your task is to carefully analyze the provided content and distill it into a brief summary that captures:

- The main topic or headline of the article.
- Key facts, events, or data mentioned.
- Any significant implications or takeaways.

Ensure the summary is:
1. Clear and easy to read.
2. Free from unnecessary details or repetition.
3. Suitable for readers who want a quick but comprehensive understanding of the article.

Content:
{content}
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

GENERATE_ARTICLE_IMAGE_PROMPT = """
You are a creative assistant tasked with generating an image to visually represent the following article. The image should be relevant to the article's content, capturing its key theme, tone, and context. 

Guidelines:
- Ensure the image reflects the article's subject matter accurately.
- Consider the emotions or ideas the article conveys and represent them visually.
- If the article mentions specific settings, objects, or people, incorporate them appropriately.
- The style of the image should be professional and engaging for a news or editorial audience.

Here is the article content:
{article}

Generate a suitable image concept based on the above.
"""

CREATE_SCRIPT_PROMPT = """Given the article below create a summary in 10 sentences focusing on the key points. Only return the summary with one sentence at each line.
Article:
{content}
"""
