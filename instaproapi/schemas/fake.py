from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class OutFake(BaseModel):
    username: str | None = None
    description: str | None = None
    subscribe_date: datetime | None = None
    data: Dict[str, str] = {}
    id: str

class InstanceTypes(str, Enum):
    user = 'USER'
    tag = 'TAG'
    location = 'LOCATION'