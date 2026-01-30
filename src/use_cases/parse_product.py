import asyncio
from urllib.parse import urlparse

from config import IHttpService
from database import AsyncSessionLocal, save_product
from models import StatusHttp
from parsers.universal_parser import UniversalParser
from services.llm_service import LLMService
from services.source_service import SourceService
from utils.url_utils import extract_domain


class ParsingError(Exception):
    pass


class ParseProductUseCase:
    def __init__(
        self,
        http_service: IHttpService,
        llm_service: LLMService,
        parser: UniversalParser,
        session_factory=AsyncSessionLocal,
    ):
        self.http_service = http_service
        self.llm_service = llm_service
        self.parser = parser
        self.session_factory = session_factory

    async def execute(self, url: str) -> dict:
        session_maker = self.session_factory

        async with session_maker() as session:
            source_service = SourceService(session)

            domain = extract_domain(url)
            source = await source_service.get_source_by_domain(domain)

            if source and source.status == StatusHttp.active:
                print(f"Используем сохраненные селекторы для {domain}")
                html_content = await self.http_service.fetch_html(url)
                selectors = source.get_selectors()
            else:
                print("Загружаем html")
                html_content = await self.http_service.fetch_html(url)
                print(f"{len(html_content)} символов")
                print("Получаем селекторы")
                selectors = await self.llm_service.get_selectors_for_html(html_content)

                if selectors:
                    source = await source_service.get_or_create_source(
                        domain, selectors
                    )
                else:
                    print("Не удалось получить селекторы от LLM для бд")
                    return {}

            print(f"Начинаем парсинг с {len(selectors)} селекторами")

            base_url = self._get_base_url(url)
            product_data = await asyncio.to_thread(
                self.parser.parse_with_selectors, html_content, selectors, base_url
            )

            product_data["origin"] = url
            await save_product(product_data, session)

            return product_data

    def _get_base_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
