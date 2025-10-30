from datetime import datetime

from typing import Optional

from sqlmodel import SQLModel, Field

from utils.ext import utc_now


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=lambda: utc_now())
    updated_at: Optional[datetime] = Field(
        nullable=True,
        default_factory=lambda: utc_now(),
        sa_column_kwargs={
            "onupdate": lambda: utc_now(),
        },
    )
    is_active: bool = Field(
        default=True,
    )
    deleted: bool = Field(
        default=False,
    )
    deleted_at: Optional[datetime] = Field(
        nullable=True,
    )
