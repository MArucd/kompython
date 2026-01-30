import traceback
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel, HttpUrl

from factory import ParserFactory

app = FastAPI(title="Parser", version="1.0")


class ParseRequest(BaseModel):
    url: HttpUrl
    force_refresh: Optional[bool] = False


class ProductData(BaseModel):
    name: str
    price: str
    images: list[str]
    description: str
    specifications: dict
    availability: str
    origin: str


class ProductResponse(BaseModel):
    success: bool
    data: Optional[ProductData] = None
    error: Optional[str] = None
    cached: bool = False


async def get_parse_product_use_case():
    return await ParserFactory.create_parse_product_use_case()


@app.get("/")
async def home():
    return {"message": ""}


@app.post("/main_parse", response_model=ProductResponse)
async def parse_product(
    request: ParseRequest, use_case=Depends(get_parse_product_use_case)
):
    try:
        url_str = str(request.url)
        product_data = await use_case.execute(url_str)

        if not product_data:
            return ProductResponse(
                success=False, error="Не удалось получить данные товара"
            )

        result = ProductData(
            name=product_data.get("name", ""),
            price=product_data.get("price", ""),
            images=product_data.get("images", []),
            description=product_data.get("description", ""),
            specifications=product_data.get("specifications", {}),
            availability=product_data.get("availability", ""),
            origin=product_data.get("origin", url_str),
        )
        return ProductResponse(success=True, data=result)

    except Exception as e:
        traceback.print_exc()
        return ProductResponse(success=False, error=f"Ошибка: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
