from config import LLM_SYSTEM_PROMPT
from llm_client import LLMClient
from utils.html_cleaner import HTMLCleaner


class LLMService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        # self.html_cleaner = html_cleaner

    async def get_selectors_for_html(self, html_content: str) -> dict:
        # cleaned_html = await self.html_cleaner.clean_for_llm(html_content)
        print("трубочисты работали всю ночь")
        return await self.llm_client.call_LLM(html_content, LLM_SYSTEM_PROMPT)
