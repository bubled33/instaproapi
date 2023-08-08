from typing import List

from pydantic import BaseModel


class InAccount(BaseModel):
    login: str
    password: str | None = None
    user_id: str

    is_fake: bool = False


class OutAccount(BaseModel):
    login: str
    password: str | None = None
    description: str | None = None
    sub_server_id: str
    actions_ids: List[str] = []
    user_id: str
    id: str

    proxy: str | None = None
    is_fake: bool = False
    fakes: List[str] = []
    owner: str | None = None

    def __str__(self) -> str:
        if self.password:
            password = f'<b>Пароль: </b><code>{"*" * len(self.password)}</code>\n'
        else:
            password = f'<b>Пароль не указан</b>\n'
        description = ''
        if self.description:
            description = f'<i>{self.description}</i>\n'

        text = ('<b>Аккаунт</b>\n'
               f'<b>Логин: </b><code>{self.login}</code>\n'
               f'{password}{description}')
               #f'<b>Кол-во действий: </b>{len(self.actions_ids)}')
        return text


    def __eq__(self, other):
        return self.id == other.id
