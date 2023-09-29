from typing import Dict, List

from pydantic import BaseModel


class InAnalyze(BaseModel):
    username: str

class OutAnalyze(BaseModel):

    id: str
    username: str
    data: Dict[str, List[str]]
    user_id: str
    is_subscribe: bool