from typing import Dict, Any

from pydantic import BaseModel

from instaproapi.schemas.server_types import ActionStatuses, ActionTypes


class InAction(BaseModel):
    action_type: ActionTypes
    account_id: str
    data: Dict[str, Any] = {}


class OutAction(BaseModel):
    id: str

    action_type: ActionTypes
    status: ActionStatuses
    account_id: str
    update_id: str
    data: Dict[str, str] = {}
    result: Any

    @property
    def button_title(self) -> str:
        return f'{ActionTypes.get_title(self.action_type)} ({ActionStatuses.get_title(self.status)})'

    async def get_info(self, subscribe_date) -> str:
        header = f'<b>Действие</b>\n' \
                 f'<b>Тип: </b><code>{ActionTypes.get_title(self.action_type)}</code>\n' \
                 f'<b>Статус: </b><code>{ActionStatuses.get_title(self.status)}</code>\n' \
                 f'<b>Оплачено до: </b> <code>{subscribe_date.strftime("%m.%d.%Y") or "Не оплачено"}</code>\n'
        content = None
        if self.action_type == ActionTypes.watch_stories:
            content = ''
        text = f'{header}{content if content else ""}'
        return text

    def __str__(self):
        text = ('<b>Действие</b>\n'
                f'<b>Тип: </b>{ActionTypes.get_title(self.action_type)}\n'
                f'<b>Статус: </b>{ActionStatuses.get_title(self.status)}\n')
        return text

    def __eq__(self, other):
        return self.id == other.id
