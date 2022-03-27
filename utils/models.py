from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from io import BytesIO
from typing import Optional

import aiohttp
from PIL import Image

from .functions import authorization_check, executor, session_check


@dataclass(slots=True, kw_only=True, repr=True)
class Cache:
    blacklist: dict = field(default_factory=dict)
    reactionroles: dict = field(default_factory=dict)

@dataclass(slots=True, repr=True, kw_only=True)
class TwitchBroadcast:
    username:       str
    broadcaster_id: int
    thumbnail:      BytesIO
    game_name:      str
    tags:           str
    started_at:     datetime.datetime
    game_image:     str
    stream_title:   str
    viewer_count:   int
    is_mature:      bool
    stream_url:     str

    @classmethod
    def from_dict(cls, json, image):
        new_json = {}
        data = json['data'][0]
        new_json['username'] = data['user_name']
        new_json['broadcaster_id'] = data['user_id']
        new_json['thumbnail'] = image
        new_json['game_name'] = data['game_name']
        new_json['tags'] = ["https://www.twitch.tv/directory/tags/" + tag for tag in data['tag_ids']]
        new_json['started_at'] = datetime.datetime.fromisoformat(data['started_at'][:-1])
        new_json['game_image'] = f"https://static-cdn.jtvnw.net/ttv-boxart/{data['game_id']}-285x380.jpg"
        new_json['stream_title'] = data['title']
        new_json['viewer_count'] = data['viewer_count']
        new_json['is_mature'] = data['is_mature']
        new_json['stream_url'] = "https://www.twitch.tv/" + data['user_name']
        return cls(**new_json)


class Twitch:
    AUTHENTICATOR = "https://id.twitch.tv/"
    BASE = "https://api.twitch.tv/"
    def __init__(self, client_id: str, client_secret: str, *, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.client_id     = client_id
        self.client_secret = client_secret
        self.authorized    = None
        self._session      = session

    @executor
    def process_image(self, image: BytesIO) -> BytesIO:
        image_overlay = Image.open('./Assets/twitch_overlay.png')
        thumbnail = Image.open(image)
        image_overlay.paste(thumbnail, (15, 10))
        buffer = BytesIO()
        image_overlay.save(buffer, "PNG")
        return buffer

    @session_check
    async def return_information(self, json) -> TwitchBroadcast:
        image = await self._session.get(json['data'][0]['thumbnail_url'].format(width=1890, height=1050))
        io_bytes = BytesIO(await image.read())
        image = await self.process_image(io_bytes)
        return TwitchBroadcast.from_dict(json, image)

    async def require_session(self) -> None:
        if not self._session:
            self._session = aiohttp.ClientSession()

    async def organize_authorized(self, json) -> None:
        token = json['access_token']
        token_type = json['token_type']
        expire_seconds = json['expires_in']
        expire_datetime_object = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_seconds)
        dictionary_object = {'datetime': expire_datetime_object, 'token': (token_type.title(), token)}
        self.authorized = dictionary_object

    @session_check
    async def authorize(self) -> None:
        params = {'client_id': self.client_id, 'client_secret': self.client_secret, 'grant_type': 'client_credentials'}
        url = self.AUTHENTICATOR + "oauth2/token"
        response = await self._session.post(url, params=params)
        json = await response.json()
        await self.organize_authorized(json)

    @session_check
    @authorization_check
    async def connect(self, endpoint, **params):
        url = self.BASE + endpoint
        authorize = " ".join(self.authorized.get('token'))
        header = {'Authorization': authorize, 'Client-Id': self.client_id}
        response = await self._session.get(url, headers=header, params=params)
        print(response.headers.get("Ratelimit-Remaining"))
        json = await response.json()
        return json

    @session_check
    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._session.close()


# async def main():
#     start = time.perf_counter()
#     async with Twitch(client_id=client_id, client_secret=client_secret) as twitch:
#         broadcaster_data = await twitch.connect("helix/users", login="projektmomo")
#         broadcaster_id   = broadcaster_data['data'][0]['id']
#         json         = await twitch.connect('helix/streams', user_id=str(broadcaster_id))
#         final_object = await twitch.return_information(json)
#         print(final_object)

# if __name__ == "__main__":
#     asyncio.run(main())

