import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from config import DATABASE_URL
from models import Base, Products

async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def find_product_by_url(url: str, db: AsyncSession):
    result = await db.execute(select(Products).where(Products.origin == url))
    return result.scalar_one_or_none()


async def save_product(product_data: dict, db: AsyncSession):
    result = await db.execute(
        select(Products).where(Products.origin == product_data["origin"])
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.name = product_data.get("name", "")
        existing.description = product_data.get("description", "")
        existing.availability = product_data.get("availability", "")

        meta_dict = {
            "price": product_data.get("price"),
            "images": product_data.get("images", []),
            "specifications": product_data.get("specifications", {}),
        }
        existing.meta = json.dumps(meta_dict, ensure_ascii=False)
    else:
        meta_dict = {
            "price": product_data.get("price"),
            "images": product_data.get("images", []),
            "specifications": product_data.get("specifications", {}),
        }

        new_product = Products(
            origin=product_data["origin"],
            name=product_data.get("name", ""),
            description=product_data.get("description", ""),
            availability=product_data.get("availability", ""),
            meta=json.dumps(meta_dict, ensure_ascii=False),
        )
        db.add(new_product)

    await db.commit()
