from typing import Dict

import httpx
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel

from config import LLM_BASE_URL


class LLMError(Exception):
    pass


class LLMNetworkError(LLMError):
    pass


class LLMResponseError(LLMError):
    pass


class ProductSelectors(BaseModel):
    name: str
    price: str
    images: str
    description: str
    specifications: str
    availability: str


class LLMClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = instructor.from_openai(
            AsyncOpenAI(api_key=api_key, base_url=LLM_BASE_URL),
            mode=instructor.Mode.MD_JSON,
        )

    async def call_LLM(self, html: str, system_prompt: str) -> Dict[str, str]:
        try:
            response = await self.client.chat.completions.create(
                model="gemini-2.5-flash-preview-09-2025",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"HTML: {html}"},
                ],
                response_model=ProductSelectors,
            )
            return response.model_dump()
        except httpx.HTTPStatusError as e:
            raise LLMNetworkError(f"HTTP error: {e}")
        except httpx.RequestError as e:
            raise LLMNetworkError(f"Request error: {e}")
        except Exception as e:
            raise LLMResponseError(f"Invalid response: {e}")
