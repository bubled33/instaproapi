from typing import List

from pydantic import BaseModel


class InSubServer(BaseModel):
    host: str
    port: int


class OutSubServer(BaseModel):
    id: str
    host: str
    port: int
    accounts_ids: List[str] = []

    def __eq__(self, other):
        return self.id == other.id
