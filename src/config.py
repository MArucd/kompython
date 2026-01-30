import os
from typing import Protocol

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SELENIUM_MAX_WORKERS = int(os.getenv("SELENIUM_MAX_WORKERS"))
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
REQUEST_TIMEOUT = 120
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

LLM_SYSTEM_PROMPT = """
TASK: Find CSS selectors in HTML for extracting product data.
Return ONLY valid JSON with these fields:

{
    "name": "CSS_selector",
    "price": "CSS_selector", 
    "images": "CSS_selector",
    "description": "CSS_selector",
    "specifications": "CSS_selector", 
    "availability": "CSS_selector"
}

IMPORTANT:
- Return ONLY JSON, NO other text
- Each selector must be valid CSS selector
- Use class selectors when possible (they're more stable)
- Use specific selectors, not too generic
- If you see MOST COMMON CLASSES section, prefer those

FIELD DESCRIPTIONS:

name - Product name/title (usually largest heading on page):
    Look for: h1, h2, or elements with classes: title, name, product-name, heading
    Must contain full product name

price - Product price in currency:
    Look for: .price, .product-price, .cost, #price
    Usually contains number and currency symbol
    Skip related prices (original, sale, etc.) - find main price

images - Product images for gallery:
    Look for: img tags in .gallery, .slider, .carousel, .product-image, .photos
    Criterion: src contains .jpg, .png, .webp, .jpeg
    Prefer elements with multiple images

description - Product description/details text:
    Look for: .description, .details, .product-details, .info, .specifications-text
    Usually longer text block describing the product

specifications - Product specs/attributes:
    Look for: .specs, .properties, .attributes, .features, .characteristics
    Often in lists (ul/ol) or tables (tbody/tr/td)
    Look for term-definition pairs (dt/dd or colons)

availability - Stock/purchase status:
    Look for: .buy, .cart, .purchase, .availability, .stock, .in-stock
    Look for buttons with text: "add to cart", "buy", "order"
    Look for status indicators: "in stock", "available", "out of stock"

HINTS:
- Check for JSON-LD structured data if exists
- Check for Open Graph meta tags
- If multiple images, use selector that gets all (not just first)
- Prefer class selectors over tag selectors
- Test selector simplicity vs specificity balance
"""



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class IHttpService(Protocol):
    async def fetch_html(self, url: str) -> str: ...

    async def close(self) -> None: ...
