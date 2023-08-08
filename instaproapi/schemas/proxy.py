from pydantic import BaseModel


class InProxy(BaseModel):
    host: str
    port: int
    username: str
    password: str

class OutProxy(BaseModel):
    id: str
    host: str
    port: int
    username: str
    password: str