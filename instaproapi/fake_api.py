#

from __future__ import annotations

import asyncio
from functools import wraps
from typing import Dict

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from .schemas.fake import InstanceTypes


class FakeAPI:
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
    async def analyze(self, instance: str, last_max_id: str | None) -> Dict[str, str]:
        params = {'instance': instance}
        if last_max_id:
            params['last_max_id'] = last_max_id
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/analyze/analyze'),
            params=params)
        return await response.json()

    @retry_async(3)
    async def unfollow(self, action_id: str, instance: str) -> Dict[str, str]:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/analyze/unfollow'),
            params={'action_id': action_id, 'instance': instance})
        return await response.json()

    @retry_async(3)
    async def like(self, account_id: str, instance: str, instance_type: InstanceTypes,
                   last_max_id: str | None = None, bio: str | None = None) -> Dict[str, str]:
        response = await self._client_session.post(
            self.base_url.format(method=f'/api/story_like/like'),
            params={'instance': instance, 'last_max_id': last_max_id, 'instance_type': instance_type,
                    'account_id': account_id, 'bio': bio})
        return await response.json()
