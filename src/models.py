import enum
import json

from sqlalchemy import JSON, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class StatusHttp(enum.Enum):
    active = "active"
    expired = "expired"


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    origin = Column(String)
    name = Column(String)
    description = Column(Text)
    availability = Column(String)
    meta = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def get_meta(self) -> dict:
        if self.meta:
            return json.loads(self.meta)
        return {}

    def set_meta(self, meta_dict: dict):
        self.meta = json.dumps(meta_dict, ensure_ascii=False)


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    domain = Column(String, unique=True)
    selectors = Column(JSON)
    status = Column(Enum(StatusHttp), default=StatusHttp.active)
    analyzed_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def get_selectors(self) -> dict:
        if isinstance(self.selectors, str):
            return json.loads(self.selectors)
        return self.selectors or {}
