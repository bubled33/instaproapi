#

from __future__ import annotations

import asyncio
from datetime import datetime
from functools import wraps
from json import JSONDecodeError
from typing import List, Dict

from aiohttp import ClientSession, TCPConnector, ContentTypeError
from loguru import logger

from .schemas.account import OutAccount
from .schemas.action import OutAction
from .schemas.analyze import OutAnalyze
from .schemas.fake import OutFake
from .schemas.proxy import OutProxy
from .schemas.server_types import ActionStatuses, ActionTypes
from .schemas.sub_server import OutSubServer
from .schemas.user import OutUser


class InstaproAPI:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._client_session: ClientSession | None = None

    async def start(self):
        connector = TCPConnector(limit=50)
        self._client_session = ClientSession(connector=connector)

    async def stop(self):
        await self._client_session.close()

    @property
    def base_url(self) -> str:
        return f'http://{self._host}:{self._port}{{method}}'

    import asyncio
    from functools import wraps
    @staticmethod
    def retry_async(num_tries):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                for i in range(num_tries):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        if i == num_tries - 1:
                            logger.error(e)
                            raise e
                        await asyncio.sleep(0.02)

            return wrapper

        return decorator

    """
    Фейки
    """

    @retry_async(3)
    async def create_fake(self, instance_id) -> OutFake:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/fakes/create'),
            json={'instance_id': instance_id})
        logger.info(await response.json())
        return OutFake(**await response.json())

    @retry_async(3)
    async def delete_fake(self, instance_id):
        await self._client_session.post(
            self.base_url.format(method=f'/api/fakes/delete'),
            json={'instance_id': instance_id})

    @retry_async(3)
    async def subscribe_fake(self, instance_id: str, days: int):
        await self._client_session.post(
            self.base_url.format(method=f'/api/fakes/subscribe'),
            json={'instance_data': {'instance_id': instance_id}, 'subscribe_data': {'days': days}})

    @retry_async(3)
    async def update_fake(self, instance_id: str, username: str | None = None, description: str | None = None):
        await self._client_session.post(
            self.base_url.format(method=f'/api/fakes/update'),
            json={'instance_data': {'instance_id': instance_id},
                  'update_data': {'username': username, 'description': description}})

    @retry_async(3)
    async def get_fake(self, instance_id):
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/fakes/get'),
            json={'instance_id': instance_id})
        response_data = await response.json()
        return OutFake(**response_data)

    async def get_fakes(self, instance_ids: List[str]) -> List[OutFake]:
        return [await self.get_fake(instance_id) for instance_id in instance_ids]

    """
    Пользователи
    """

    @retry_async(3)
    async def get_subscribe_date(self, instance_id: str, action_type: ActionTypes,
                                 account_id: str | None = None) -> datetime | None:
        user = await self.get_user(instance_id)
        for subscribe in user.subscribes:
            if subscribe.account_id == account_id and subscribe.action_type == action_type:
                return subscribe.subscribe_date
        return None

    @retry_async(3)
    async def subscribe(self, instance_id: str, action_type: ActionTypes, days: int, account_id: str | None = None):
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/users/subscribe'),
            json={'instance_id': instance_id, 'action_type': action_type,
                  'days': days, 'account_id': account_id}
        )

    @retry_async(3)
    async def create_user(self, telegram_id: int) -> OutUser:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/users/create'),
            json={'telegram_id': telegram_id})
        logger.info(await response.json())
        return OutUser(**await response.json())

    @retry_async(3)
    async def get_user_by_telegram_id(self, telegram_id: int) -> OutUser | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/users/get_by_telegram_id'), json={'telegram_id': telegram_id})
        data = await response.json()
        if not data:
            return None
        return OutUser(**data)

    @retry_async(3)
    async def get_user(self, instance_id: str) -> OutUser:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/users/get?instance_id={instance_id}'), json={'instance_id': instance_id})
        return OutUser(**await response.json())

    @retry_async(3)
    async def get_all(self) -> List[OutUser]:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/users/get_all'))
        return [OutUser(**data) for data in await response.json()]

    @retry_async(3)
    async def delete_user(self, instance_id: str):
        await self._client_session.post(
            self.base_url.format(method=f'/api/users/delete'), json={'instance_id': instance_id})

    """"
    Анализ
    """

    @retry_async(3)
    async def create_analyze(self, user_id: str, username: str) -> OutAnalyze:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/analyze/create'),
            json={'instance_data': {'username': username}, 'user_data': {'instance_id': user_id}})
        return OutAnalyze(**await response.json())

    @retry_async(3)
    async def update_analyze(self, instance_id: str, key: str, values: List[str]) -> OutAnalyze:
        await self._client_session.post(
            self.base_url.format(method=f'/api/analyze/update'),
            json={'instance_data': {'instance_id': instance_id}, 'update_analyze': {'key': key,
                                                                                    'values': values}})

    @retry_async(3)
    async def subscribe_analyze(self, instance_id: str):
        await self._client_session.post(
            self.base_url.format(method=f'/api/analyze/subscribe'),
            json={'instance_id': instance_id})

    @retry_async(3)
    async def get_analyze(self, instance_id: str):
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/analyze/get'),
            json={'instance_id': instance_id})

        return OutAnalyze(**await response.json())

    """
    Акаунты
    """

    @retry_async(3)
    async def update_account(self, instance_id: str, username: str | None = None, password: str | None = None,
                             description: str | None = None):
        await self._client_session.post(self.base_url.format(method=f'/api/accounts/update'),
                                        json={'instance_id': instance_id, 'username': username, 'password': password,
                                              'description': description})

    @retry_async(3)
    async def create_account(self, user_id: str, login: str, is_fake: bool = False) -> OutAccount:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/accounts/create'),
            json={'login': login, 'user_id': user_id, 'is_fake': is_fake})
        return OutAccount(**await response.json())

    @retry_async(3)
    async def add_fake(self, instance_id: str) -> OutAccount | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/accounts/add_fake'),
            json={'instance_id': instance_id})
        try:
            response_data = await response.json()
        except (ContentTypeError, JSONDecodeError) as e:
            return None
        if not response_data:
            return None
        return OutAccount(**response_data)

    @retry_async(3)
    async def remove_fake(self, instance_id: str, fake_id: str):
        await self._client_session.post(
            self.base_url.format(method=f'/api/accounts/remove_fake'),
            json={'instance_id': instance_id, 'fake_id': fake_id})

    @retry_async(3)
    async def delete_account(self, instance_id: str):
        await self._client_session.post(
            self.base_url.format(method=f'/api/accounts/delete'), json={'instance_id': instance_id})

    @retry_async(3)
    async def get_account(self, instance_id: str) -> OutAccount | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/accounts/get'), json={'instance_id': instance_id})
        data = await response.json()
        if not data:
            return None
        return OutAccount(**await response.json())

    """
    Действия
    """

    @retry_async(3)
    async def create_action(self, account_id: str, action_type: ActionTypes,
                            data: Dict[str, str] | None = None) -> OutAction:
        if data is None:
            data = dict()

        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/create'), json={'account_id': account_id, 'action_type': action_type,
                                                      'data': data}
        )
        print(await response.json())
        return OutAction(**await response.json())

    @retry_async(3)
    async def get_action_queue(self, instance_id: str) -> OutAction | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/actions/get_queue'),
            json={'instance_id': instance_id}
        )
        try:
            data = await response.json()
        except (JSONDecodeError, ContentTypeError):
            return None
        if not data:
            return None
        return OutAction(**data)

    @retry_async(3)
    async def get_action(self, instance_id: str) -> OutAction:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/actions/get'), json={'instance_id': instance_id}
        )
        return OutAction(**await response.json())

    @retry_async(3)
    async def get_all_action_by_account(self, instance_id: str) -> List[OutAction]:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/actions/get_all_by_account', json={'instance_id': instance_id})
        )
        return [OutAction(**data) for data in await response.json()]

    @retry_async(3)
    async def set_status(self, instance_id: str, status: ActionStatuses):
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/actions/set_status'), json={'status': status, 'instance_id': instance_id}
        )
        logger.info(await response.json())
        return await response.json()

    @retry_async(3)
    async def set_result(self, instance_id: str, key: str, value: str):
        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/set_result'
            ), json={'key': key, 'value': value, 'instance_id': instance_id})

        return await response.json()

    @retry_async(3)
    async def get_result(self, instance_id: str, key: str):
        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/get_result'
            ), json={'key': key, 'instance_id': instance_id})
        res = await response.text()
        return res.replace('"', '') if res != 'null' else None

    @retry_async(3)
    async def delete_result(self, instance_id: str, key: str):
        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/delete_result'
            ), json={'key': key, 'instance_id': instance_id}
        )

    @retry_async(3)
    async def set_data(self, instance_id: str, key: str, value: str):
        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/set_data'
            ), json={'key': key, 'value': value, 'instance_id': instance_id})

        return await response.json()

    @retry_async(3)
    async def get_data(self, instance_id: str, key: str) -> str | None:
        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/get_data'
            ), json={'key': key, 'instance_id': instance_id})

        res = await response.text()
        return res.replace('"', '') if res != 'null' else None

    @retry_async(3)
    async def delete_data(self, instance_id: str, key: str):
        response = await self._client_session.post(
            self.base_url.format(
                method=f'/api/actions/delete_data'
            ), json={'key': key, 'instance_id': instance_id}
        )

    """
    Прокси
    """

    @retry_async(3)
    async def create_proxy(self, host: str, port: int, username: str, password: str) -> OutProxy:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/proxy/create'), json={'host': host, 'port': port,
                                                                     'username': username, 'password': password}
        )
        logger.info(await response.json())
        return OutProxy(**await response.json())

    @retry_async(3)
    async def get_proxy(self, instance_id: str) -> OutProxy | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/proxy/get'), json={'instance_id': instance_id}
        )
        response_data = await response.json()
        if not response_data:
            return None
        return OutProxy(**await response.json())

    @retry_async(3)
    async def get_queue_proxy(self) -> OutProxy | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/sub_servers/get_queue')
        )
        if not (await response.json()):
            return None
        return OutSubServer(**await response.json())

    """
    Сабсерверы
    """

    @retry_async(3)
    async def create_sub_server(self, host: str, port: int) -> OutSubServer:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/sub_servers/create'), json={'host': host, 'port': port}
        )
        logger.info(await response.json())
        return OutSubServer(**await response.json())

    @retry_async(3)
    async def get_sub_server(self, instance_id: str) -> OutSubServer:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/sub_servers/get'), json={'instance_id': instance_id}
        )
        return OutSubServer(**await response.json())

    @retry_async(3)
    async def get_queue_sub_server(self) -> OutSubServer | None:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/sub_servers/get_queue')
        )
        if not (await response.json()):
            return None
        return OutSubServer(**await response.json())

    @retry_async(3)
    async def get_all_sub_servers(self) -> List[OutSubServer]:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/sub_servers/get')
        )
        logger.info(await response.json())
        return [OutSubServer(**data) for data in await response.json()]

    @retry_async(3)
    async def delete_sub_server(self, instance_id: str):
        await self._client_session.post(
            self.base_url.format(method=f'/api/sub_servers/delete'), json={'instance_id': instance_id}
        )

    """
    Остальное
    """

    @retry_async(3)
    async def send_error(self, instance_id: str):
        action = await self.get_action(instance_id=instance_id)
        account = await self.get_account(action.account_id)
        user = await self.get_user(account.user_id)
        text = ("<b>Ошибка</b>\n"
                f"<b>Аккаунт: </b><code>{account.login}</code>\n"
                f"<b>Действие: </b><code>{ActionTypes.get_title(action.action_type)}</code>\n"
                f"<b>Текущий статус: </b><code>{ActionStatuses.get_title(action.status)}</code>"
                )
        await self._bot.send_message(chat_id=user.telegram_id, text=text)

    @retry_async(3)
    async def send_code_request(self, instance_id: str):
        text = (f'<b>Введите код из письма</b>\n#Service info\nAction ID: {instance_id}')
        action = await self.get_action(instance_id=instance_id)
        account = await self.get_account(action.account_id)
        user = await self.get_user(account.user_id)
        await self._bot.send_message(chat_id=user.telegram_id, text=text)

    @retry_async(3)
    async def send_submit_request(self, instance_id: str):
        pass

    @retry_async(3)
    async def get_accounts(self, instances_ids: List[str]) -> List[OutAccount]:
        result = []
        for instance_id in instances_ids:
            result.append(await self.get_account(instance_id))

        return result

    @retry_async(3)
    async def get_actions(self, instances_ids: List[str]) -> List[OutAction]:
        result = []
        for instance_id in instances_ids:
            result.append(await self.get_action(instance_id))

        return result
