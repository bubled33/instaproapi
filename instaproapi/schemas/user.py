from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel

from instaproapi.schemas.server_types import ActionTypes


class Subscribe(BaseModel):
    action_type: ActionTypes
    account_id: str | None = None
    subscribe_date: datetime


class InUser(BaseModel):
    telegram_id: int


class OutUser(BaseModel):
    telegram_id: int
    id: str
    accounts_ids: List[str] = []
    subscribes: List[Subscribe] = []
    fakes: List[str] = []
