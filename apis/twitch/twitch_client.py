from __future__ import annotations

"""
Module `twitch_client` contains the `TwitchClient` class, which is used to
interact with the Twitch API to fetch and process data from it.
"""

import aiohttp
import datetime

from apis import twitch
from typing import Any, Optional, Final
from io import BytesIO
from PIL import Image


class TwitchClient:
    """
    Class `Twitch` is a wrapper for the Twitch API. It provides methods that
    can connect to a Twitch API endpoint and return API responses as an object.
    """
    AUTH_URL: Final = "https://id.twitch.tv/"
    BASE_URL: Final = "https://api.twitch.tv/"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        session: Optional[aiohttp.ClientSession]=None,
    ) -> None:
        """
        Creates an instance of `Twitch` that can be used to interact with
        the Twitch API. Connects to a Twitch API endpoint and returns data
        about streams using a TwitchBroadcast instance.

        Params:
         - client_id (str): The Twitch API application's ID.
         - client_secret (str): The Twitch API application's secret.
         - session (aiohttp.ClientSession): The client session to use (Optional).

        Returns:
         - A `Twitch` instance.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorized: dict[str, Any] = None
        self._session = session

    @twitch.decorators.session_check
    @twitch.decorators.authorization_check
    async def connect(self, endpoint: str, **params: dict) -> dict:
        """
        Connects to a Twitch API endpoint that we can use to get data
        about twitch broadcasts.

        Params:
         - endpoint (str): The Twitch API endpoint to connect to.
         - **params (dict): The parameters to pass to the HTTP get request.

        Returns:
         - A JSON document containing the data returned from the HTTP request.
        """
        url = self.BASE_URL + endpoint
        authorize = " ".join(self.authorized.get("token"))

        header = {
            "Authorization": authorize,
            "Client-Id": self.client_id
        }

        response = await self._session.get(url, headers=header, params=params)
        json = await response.json()

        return json

    @twitch.decorators.session_check
    async def get_broadcast(self, json: dict) -> twitch.TwitchBroadcast:
        """
        Creates a `TwitchBroadcast` instance containing information returned
        from a Twitch API response. See the documentation for `TwitchBroadcast`
        for more information.
        """
        url = json["data"][0]["thumbnail_url"].format(width=1890, height=1050)

        image = await self._session.get(url)
        bytes = BytesIO(await image.read())
        image = await self.__process_image(bytes)

        return twitch.TwitchBroadcast.from_dictionary(json, image)

    @twitch.decorators.session_check
    async def __aenter__(self) -> TwitchClient:
        """
        Dunder method that defines what happens when an async with
        statement using an instance of this class is entered.
        """
        return self

    async def __aexit__(self, *excinfo) -> None:
        """
        Dunder method that defines what happens when an async with
        statement using an instance of this class is exited.
        """
        await self._session.close()

    async def __require_session(self) -> None:
        """
        Internal method that creates an aiohttp.ClientSession and assigns
        it to self._session. This method is not called in this class, and
        is instead called by @decorators.session_check.
        """
        if not self._session:
            self._session = aiohttp.ClientSession()

    @twitch.decorators.executor
    def __process_image(self, image: BytesIO) -> BytesIO:
        """
        Internal method that processes a Twitch stream's thumbnail by
        pasting it on top of an overlay image and then centering it.

        Params:
         - image (BytesIO): The image to paste on top of the overlay.

        Returns:
         - A `BytesIO` object containing the image pasted onto the overlay.
        """
        OVERLAY_FILEPATH: Final = "./assets/twitch_overlay.png"

        overlay = Image.open(OVERLAY_FILEPATH)
        thumbnail = Image.open(image)

        buffer = BytesIO()
        overlay.paste(thumbnail, (15, 10))
        overlay.save(buffer, "PNG")

        return buffer

    @twitch.decorators.session_check
    async def __authorize(self) -> None:
        """
        Internal method that uses the `TwitchClient` instance's API application
        ID and secret to authenticate HTTP get requests.
        """
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        url = self.AUTH_URL + "oauth2/token"
        response = await self._session.post(url, params=params)
        json = await response.json()

        await self.__organize_authorized(json)

    async def __organize_authorized(self, json: dict) -> None:
        """
        Internal method that sets the value of self.authorized to a dictionary
        containing the access token, token type, and the date/time when the
        authorization expires.
        """
        access_token = json["access_token"]
        token_type = json["token_type"]
        expires_in = json["expires_in"]

        authorization_information = {
            "datetime":  datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
            "token": (token_type.title(), access_token),
        }

        self.authorized = authorization_information