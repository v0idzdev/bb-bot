import datetime

from io import BytesIO
from dataclasses import dataclass


@dataclass(slots=True, repr=True, kw_only=True)
class TwitchBroadcast:
    username: str
    broadcaster_id: int
    thumbnail: BytesIO
    game_name: str
    tags: str
    started_at: datetime.datetime
    game_image: str
    stream_title: str
    viewer_count: int
    is_mature: bool
    stream_url: str

    @classmethod
    def from_dict(cls, json, image):
        new_json = {}
        data = json["data"][0]

        new_json["username"] = data["user_name"]
        new_json["broadcaster_id"] = data["user_id"]
        new_json["thumbnail"] = image
        new_json["game_name"] = data["game_name"]
        new_json["tags"] = [
            "https://www.twitch.tv/directory/tags/" + tag for tag in data["tag_ids"]
        ]

        new_json["started_at"] = datetime.datetime.fromisoformat(
            data["started_at"][:-1]
        )

        new_json[
            "game_image"
        ] = f"https://static-cdn.jtvnw.net/ttv-boxart/{data['game_id']}-285x380.jpg"

        new_json["stream_title"] = data["title"]
        new_json["viewer_count"] = data["viewer_count"]
        new_json["is_mature"] = data["is_mature"]
        new_json["stream_url"] = "https://www.twitch.tv/" + data["user_name"]

        return cls(**new_json)
