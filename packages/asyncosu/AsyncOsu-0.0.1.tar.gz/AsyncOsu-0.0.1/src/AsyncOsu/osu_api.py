import asyncio
import logging
from datetime import datetime, timedelta
from types import TracebackType
from typing import List, Dict, Optional, Type

import aiohttp

logger = logging.getLogger('AsyncOsu')
logger.addHandler(logging.NullHandler())


class OsuApiV2:

    def __init__(self, client_id, client_secret):
        self._osu_client_id = client_id
        self._osu_client_secret = client_secret

        self._osu_access_token = None
        self._access_token_obtain_date = None
        self._access_token_expire_date = None
        self._client_session: Optional[aiohttp.ClientSession] = None

        self._osu_api_cooldown = 1
        self._last_request_time = datetime.now()

        return

    async def get_user_best_ranks(self, user_id: int, limit: int = 25) -> List[Dict]:
        """
        This endpoint returns the scores of specified user.
        :param user_id: Id of the user.
        :param limit: Maximum number of results.
        :return: Array of Score.
        """
        params = {'mode': 'osu',
                  'limit': limit}
        logger.debug(f'Requesting user best ranks with {params}')
        return await self._get_endpoint(f'users/{user_id}/scores/best', params)

    async def get_country_top_50(self, country_code: str, game_mode: str = 'osu'):
        """
        Gets the current ranking for the specified type and game mode.
        :param country_code: Filter ranking by country code.
        :param game_mode: Game mode. One of [fruits, mania, osu, taiko]
        :return: Returns Rankings
        """
        params = {'country': country_code}
        logger.debug(f'Requesting country top player list with {params}')
        return await self._get_endpoint(f'rankings/{game_mode}/performance', params)

    async def get_beatmap_info(self, beatmap_id: int):
        """
        Gets beatmap data for the specified beatmap ID.
        :param beatmap_id: The ID of the beatmap.
        :return: Returns Beatmap object.
        """
        logger.debug(f'Requesting beatmap information for id: {beatmap_id}')
        return await self._get_endpoint(f'beatmaps/{beatmap_id}')

    async def get_user_from_id(self, user_id: int, game_mode: Optional[str] = None):
        """
        This endpoint returns the detail of specified user.
        It's highly recommended to pass key parameter to avoid getting unexpected result
        (mainly when looking up user with numeric username or nonexistent user id).
        :param user_id: Id of the user.
        :param game_mode: GameMode. User default mode will be used if not specified.
        :return:
        """

        logger.debug(f'Requesting user information for id: {user_id}')
        params = {'key': 'id'}
        endpoint = f'users/{user_id}/{game_mode}' if game_mode else f'users/{user_id}'
        return await self._get_endpoint(endpoint=endpoint, params=params)

    async def get_user_from_username(self, username: str, game_mode: str = 'osu'):
        """
        This endpoint returns the detail of specified user.
        It's highly recommended to pass key parameter to avoid getting unexpected result
        (mainly when looking up user with numeric username or nonexistent user id).
        :param user_id: Id of the user.
        :return:
        """

        logger.debug(f'Requesting user information for username: {username}')
        params = {'key': 'username'}
        endpoint = f'users/{username}/{game_mode}' if game_mode else f'users/{username}'
        return await self._get_endpoint(endpoint=endpoint, params=params)

    async def get_beatmap_bytes(self, beatmap_id: int):
        """
        Gets the beatmap bytes from osu! http endpoint. THIS IS NOT AN API CALL.
        :param beatmap_id: Id of the beatmap.
        :return:
        """
        logger.debug(f'Requesting beatmap bytes for id: {beatmap_id}')
        async with aiohttp.ClientSession() as c:
            async with c.get(f'https://osu.ppy.sh/osu/{beatmap_id}') as resp:
                contents = await resp.read()
        return contents

    async def _get_endpoint(self, endpoint: str, params: dict = None) -> List:
        if self._osu_access_token is None or await self._check_token_expired():
            await self._get_access_token()

        seconds_since_last_request = (datetime.now() - self._last_request_time).total_seconds()
        if seconds_since_last_request < self._osu_api_cooldown:
            await asyncio.sleep(self._osu_api_cooldown - seconds_since_last_request)

        async with self._client_session.get(f'https://osu.ppy.sh/api/v2/{endpoint}', params=params) as resp:
            contents = await resp.json()

        self._last_request_time = datetime.now()

        return contents

    async def _get_access_token(self):
        params = {'client_id': self._osu_client_id,
                  'client_secret': self._osu_client_secret,
                  'grant_type': 'client_credentials',
                  'scope': 'public'}

        async with aiohttp.ClientSession() as c:
            async with c.post('https://osu.ppy.sh/oauth/token', json=params) as r:
                token_response = await r.json()

        self._osu_access_token = token_response['access_token']
        self._access_token_obtain_date = datetime.now()
        self._access_token_expire_date = self._access_token_obtain_date + timedelta(
            seconds=token_response['expires_in'])

        headers = {'Authorization': f'Bearer {self._osu_access_token}'}
        self._client_session = aiohttp.ClientSession(headers=headers)

    async def _check_token_expired(self):
        return datetime.now() + timedelta(seconds=100) > self._access_token_expire_date

    async def close(self):
        if self._client_session is not None:
            await self._client_session.close()

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    async def __aenter__(self) -> "OsuApiV2":
        await self._get_access_token()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        await self._client_session.close()

    def __del__(self):
        if not self._client_session.closed:
            logger.warning(f'Client session is not closed! You should use await {self.__name__}.close(),'
                           f' or use a context manager before deleting this instance. If more objects created, '
                           f'this will lead to resource exhaustion.')
            return
