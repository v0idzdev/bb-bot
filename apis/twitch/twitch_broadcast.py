from __future__ import annotations

"""
Module `twitch_broadcast` includes class `TwitchBroadcast`, which
is used to store a Twitch API response in a way that makes it easier
to work with, by accessing data as an attribute of the class instead
of working with a Dictionary.
"""

import datetime

from io import BytesIO
from dataclasses import dataclass, field


@dataclass(slots=True, repr=True, kw_only=True)
class TwitchBroadcast:
    """
    Class `TwitchBroadcast` is a @dataclass used to store data
    returned from a Twitch API response. This class should not be
    instantiated directly with TwitchBroadcast.from_dictionary.

    Instead, call Twitch.create_twitch_broadcast. This will ensure
    the class has been initialized correctly.

    Attributes:
     - user_name (str): The name of the broadcaster.
     - user_id (str): The ID of the broadcaster.
     - thumbnail (str): The processed thumbnail with an overlay.
     - game_name (str): The name of the game being streamed.
     - title: (str): The title of the stream.
     - start: (datetime): The stream's start time.
     - url: (str): A URL link to the stream.
     - viewer_count (int): The number of viewers the stream has.
     - is_mature (bool): Whether the stream is 18+.
    """
    user_name: str
    user_id: int
    thumbnail: BytesIO
    game_name: str
    game_image: str
    title: str
    start: datetime.datetime
    url: str
    viewer_count: int
    is_mature: bool

    @classmethod
    def from_dictionary(cls, response: dict, image: BytesIO) -> TwitchBroadcast:
        """
        Creates an instance of `TwitchBroadcast` from a JSON document returned
        from a Twitch API response. This method acts as a constructor for the
        class, and is used as such: TwitchBroadcast.from_dictionary.

        Params:
         - response (dict): The JSON document the Twitch API returned.
         - image (BytesIO): The processed image to be used in a Discord embed.

        Returns:
         - A `TwitchBroadcast` instance.
        """
        response = response["data"][0]
        arguments = {}

        # For all of the items in the response that are also attributes of this
        # class, simply assign the attributes the values of the items.
        for key, value in vars(cls).iteritems():
            if key in response:
                arguments[key] = value

        # Some attributes need to be processed first, so do that here.
        arguments["thumbnail"] = cls.__generate_thumbnail(response["game_id"])
        arguments["stream_link"] = cls.__generate_stream_url(response["user_name"])
        arguments["stream_start"] = cls.__generate_stream_start(response["started_at"])

        return cls(**arguments)

    @staticmethod
    def __generate_stream_url(user_name: str) -> str:
        """
        Internal method that returns a URL that users can use to watch the
        stream described by an instance of this class.
        """
        return "https://www.twitch.tv/" + user_name

    @staticmethod
    def __generate_stream_start(started_at: str) -> datetime:
        """
        Internal method that processes the start time for the stream returned
        by the Twitch API in ISO format. Returns a datetime object.
        """
        return datetime.datetime.fromisoformat(started_at[:-1])

    @staticmethod
    def __generate_thumbnail(game_id: str) -> str:
        """
        Internal method that returns a URL where the game image is hosted. We
        can use this image to generate an image in a Discord message or embed.
        """
        return "https://static-cdn.jtvnw.net/ttv-boxart/" + game_id + "-285x380.jpg"