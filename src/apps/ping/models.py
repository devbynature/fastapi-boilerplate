from sqlmodel import Field
from beanie import Document

from typing import Optional

from utils.common_models import BaseModel


class TestModel(BaseModel, table=True):
    id: Optional[int] = Field(
        primary_key=True,
    )


class TestDocument(Document):
    name: str
