"""
Module `discord_client_factory` contains the class
`DiscordClientFactory`, which is used to instantiate
`DiscordClient` objects.
"""
from __future__ import annotations
from core.discord_client import DiscordClient

import itertools

from typing import (
    List,
    Dict,
    Any
)


class DiscordClientFactory:
    """
    Class `DiscordClientFactory` is used to instantiate
    `DiscordClient` objects via method calls.
    """
    def __init__(self) -> None:
        """
        Creates an instance of `DiscordClientFactory`. Ensure that you
        add the correct attributes using the appropriate methods.

        Returns:
         - A `DiscordClientFactory` instance.
        """
        ...

    def create_discord_client(
        self,
        possible_statuses: itertools.cycle,
        extension_filepaths: List[str],
        handler_filepaths: List[str],
        testing_guild_ids: List[int],
        twitch_client_id: str,
        twitch_client_secret: str,
        mongo_connection_url: str,
        **kwargs: Dict[str, Any]
    ) -> DiscordClient:
        """
        Creates an instance of `DiscordClient` that is used to interact with
        Discord, and is responsible for loading & starting the bot, and
        syncing slash commands.

        Params:
         - possible_statuses (itertools.Cycle): A list of statuses the bot will cycle through.
         - extension_filepaths (list[str]): The filepaths of cogs the bot will use.
         - handler_filepaths (list[str]): The filepaths of handlers the bot will use.
         - testing_guild_ids (list[int]): The IDs of testing guilds the bot is in.
         - mongo_connection_url (str): The URL used to connect to a MongoDB database.
         - twitch_client_id (str): The Twitch API application's ID.
         - twitch_client_secret (str): The Twitch API application's secret.

        Returns:
         - A `DiscordClient` instance.
        """
        return DiscordClient(
            possible_statuses,
            extension_filepaths,
            handler_filepaths,
            testing_guild_ids,
            twitch_client_id,
            twitch_client_secret,
            mongo_connection_url,
            **kwargs
        )