import aiohttp
import datetime

from io import BytesIO
from typing import Optional
from PIL import Image
from utils.models import TwitchBroadcast
from utils.functions import executor, session_check, authorization_check


class Twitch:
    AUTHENTICATOR = "https://id.twitch.tv/"
    BASE = "https://api.twitch.tv/"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorized = None
        self._session = session

    @executor
    def process_image(self, image: BytesIO) -> BytesIO:
        image_overlay = Image.open("./assets/twitch_overlay.png")
        thumbnail = Image.open(image)
        image_overlay.paste(thumbnail, (15, 10))
        buffer = BytesIO()
        image_overlay.save(buffer, "PNG")

        return buffer

    @session_check
    async def return_information(self, json) -> TwitchBroadcast:
        image = await self._session.get(
            json["data"][0]["thumbnail_url"].format(width=1890, height=1050)
        )

        io_bytes = BytesIO(await image.read())
        image = await self.process_image(io_bytes)
        return TwitchBroadcast.from_dict(json, image)

    async def require_session(self) -> None:
        if not self._session:
            self._session = aiohttp.ClientSession()

    async def organize_authorized(self, json) -> None:
        token = json["access_token"]
        token_type = json["token_type"]
        expire_seconds = json["expires_in"]
        expire_datetime_object = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=expire_seconds
        )

        dictionary_object = {
            "datetime": expire_datetime_object,
            "token": (token_type.title(), token),
        }

        self.authorized = dictionary_object

    @session_check
    async def authorize(self) -> None:
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        url = self.AUTHENTICATOR + "oauth2/token"
        response = await self._session.post(url, params=params)
        json = await response.json()

        await self.organize_authorized(json)

    @session_check
    @authorization_check
    async def connect(self, endpoint, **params):
        url = self.BASE + endpoint
        authorize = " ".join(self.authorized.get("token"))
        header = {"Authorization": authorize, "Client-Id": self.client_id}
        response = await self._session.get(url, headers=header, params=params)

        print(response.headers.get("Ratelimit-Remaining"))
        json = await response.json()

        return json

    @session_check
    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._session.close()
