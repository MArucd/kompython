from config import DEEPSEEK_API_KEY, GEMINI_API_KEY
from database import AsyncSessionLocal
from llm_client import LLMClient
from parsers.universal_parser import UniversalParser
from services.llm_service import LLMService
from services.selenium_service import SeleniumService
from use_cases.parse_product import ParseProductUseCase
from utils.html_cleaner import HTMLCleaner

class ParserFactory:
    @staticmethod
    async def create_parse_product_use_case():
        selenium_service = SeleniumService(headless=True, timeout=300)
        llm_client = LLMClient(api_key=GEMINI_API_KEY)
        llm_service = LLMService(llm_client)
        parser = UniversalParser()

        return ParseProductUseCase(
            http_service=selenium_service,
            llm_service=llm_service,

            parser=parser,
            session_factory=lambda: AsyncSessionLocal(),
        )
