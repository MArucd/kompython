import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config import SELENIUM_MAX_WORKERS, USER_AGENT, IHttpService


class SeleniumService(IHttpService):
    def __init__(
        self, headless: bool = True, timeout: int = 300, save_dir: str = "selres"
    ):
        self.headless = headless
        self.timeout = timeout
        self.save_dir = save_dir
        self.executor = ThreadPoolExecutor(max_workers=SELENIUM_MAX_WORKERS)
        os.makedirs(save_dir, exist_ok=True)

    def _extract_domain(self, url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")

    def _init_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={USER_AGENT}")
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(self.timeout)
        return driver

    def _fetch_html_sync(self, url: str) -> str:
        driver = self._init_driver()
        domain = self._extract_domain(url)

        try:
            driver.get(url)
            WebDriverWait(driver, self.timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(10)
            html_content = driver.page_source
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{self.save_dir}/{domain.replace('.', '_')}_{timestamp}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)

            return html_content
        finally:
            driver.quit()

    async def fetch_html(self, url: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._fetch_html_sync, url)

    async def close(self):
        self.executor.shutdown(wait=True)
