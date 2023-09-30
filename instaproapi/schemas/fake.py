from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class OutFake(BaseModel):
    username: str | None = None
    description: str | None = None
    subscribe_date: datetime | None = None
    id: str

class InstanceTypes(str, Enum):
    user = 'USER'
    tag = 'TAG'
    location = 'LOCATION'