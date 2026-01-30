from typing import Dict, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Source, StatusHttp


class SourceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_source_by_domain(self, domain: str) -> Optional[Source]:
        result = await self.db.execute(select(Source).where(Source.domain == domain))
        return result.scalar_one_or_none()

    async def create_source(self, domain: str, selectors: Dict[str, str]) -> Source:
        try:
            source = Source(domain=domain, selectors=selectors)
            self.db.add(source)
            await self.db.commit()
            await self.db.refresh(source)
            return source
        except IntegrityError:
            await self.db.rollback()
            return await self.get_source_by_domain(domain)

    async def get_or_create_source(
        self, domain: str, selectors: Dict[str, str]
    ) -> Source:
        source = await self.get_source_by_domain(domain)

        if source:
            await self.update_source_selectors(source, selectors)
            return source
        else:
            return await self.create_source(domain, selectors)

    async def update_source_selectors(
        self, source: Source, new_selectors: dict
    ) -> None:
        source.selectors = new_selectors
        source.status = StatusHttp.active
        source.analyzed_at = func.now()
        await self.db.commit()
