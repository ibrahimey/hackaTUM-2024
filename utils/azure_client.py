import os

from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI

load_dotenv()


class AzureOpenAIClient:
    def __init__(self, temperature, top_p) -> None:
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_GPT_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_GPT_API_VERSION"),
            api_key=os.getenv("AZURE_OPENAI_GPT_API_KEY"),
            temperature=temperature,
            top_p=top_p,
        )

    def __call__(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content
