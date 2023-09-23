from datetime import datetime

from pydantic import BaseModel


class OutFake(BaseModel):
    username: str | None = None
    description: str | None = None
    subscribe_date: datetime | None = None