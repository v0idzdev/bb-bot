"""
Module `discord_client` contains the `DiscordClient` class, which is
responsible for loading extensions, syncing application commands against
the Discord API, and starting the bot.
"""
from __future__ import annotations

import aiohttp
import discord
import itertools
import twitchio
import toml

from core.utils.aliases import MongoClient
from discord.ext import commands
from typing import (
    List,
    Dict,
    Any
)


class DiscordClient(commands.Bot):
    """
    Class `DiscordClient` creates an instance of BB.Bot that loads
    extensions, syncs application commands, and starts the bot.
    """
    def __init__(
        self,
        status: str,
        theme: int,
        extension_filepaths: List[str],
        test_guild_ids: List[int],
        mongo_client: MongoClient,
        twitch_client: twitchio.Client,
        **kwargs: Dict[str, Any]
    ) -> None:
        """
        Creates an instance of `DiscordClient` that is used to interact with
        Discord, and is responsible for loading & starting the bot, and
        syncing slash commands.

        Params:return 
         - possible_statuses (itertools.Cycle): A list of statuses the bot will cycle through.
         - extension_filepaths (list[str]): The filepaths of extensions the bot will use.
         - testing_guild_ids (list[int]): The IDs of testing guilds the bot is in.
         - mongo_connection_url (str): The URL used to connect to a MongoDB database.
         - twitch_client_id (str): The Twitch API return application's ID.
         - twitch_client_secret (str): The Twitch API application's secret.

        Returns:
         - A `DiscordClient` instance.
        """
        super().__init__(**kwargs)

        self.theme = int(theme, 16)
        self._status = status
        self._session: aiohttp.ClientSession = None
        self._extension_filepaths = extension_filepaths
        self._test_guild_ids = test_guild_ids
        self._twitch_client = twitch_client
        self._mongo_client = mongo_client

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Returns the value of self._session. This stops the value being set
        from outside the `Client` class.
        """
        return self._session

    @property
    def extension_filepaths(self) -> List[str]:
        """
        Returns the value of self._extension_filepaths. This stops the value
        being set from outside the `Client` class.
        """
        return self._extension_filepaths
    
    @property
    def test_guild_ids(self) -> List[int]:
        """
        Returns the value of self._twitch_client. This stops the value
        being set from outside the `Client` class.
        """
        return self._test_guild_ids

    @property
    def mongo_client(self) -> MongoClient:
        """
        Returns the value of self._mongo_client. This stops the value
        being set from outside the `Client` class. Access databases the
        client has access to by using self.mongo_client["database_name"].

        To use this with the module `apis.mongo.collection` (i.e, to edit
        a table), use apis.mongo.Collection(self.mongo_client["name"], "table")
        """
        return self._mongo_client

    @property
    def twitch_client(self) -> twitchio.Client:
        """
        Returns the value of self._twitch_client. This stops the value
        being set from outside the `Client` class.
        """
        return self._twitch_client

    async def start_pipeline(self, token: str) -> None:
        """
        Calls `.__load()`, `.__sync()`, and `.__start()`. Starts the pipeline of processes
        that initialise, sync, and log in to the bot. 

        Params:
         - token (str): The Discord token used to log into a bot account.
        """
        async with self:
            await self.__load()
            self.loop.create_task(self.__sync())
            await self.__start(token)

    async def __start(self, *args, **kwargs) -> None:
        """
        Overrides commands.Bot.start to create a re-usable aiohttp.ClientSession, and to
        create TwitchClient and MongoClient instances. Use this method to start the bot.
        """
        async with aiohttp.ClientSession() as self._session:
            await super().start(*args, **kwargs)

    async def __sync(self) -> None:
        """
        Synchronizes application commands the bot uses with Discord. For any server/guild
        with an ID in `self.__testing_guild_ids`, slash commands will be synced instantly.
        For all other guilds, this may take up to an hour to complete.
        """
        await self.wait_until_ready()

        for test_guild_id in self._test_guild_ids:
            await self.tree.sync(guild=discord.Object(id=test_guild_id))

        await self.tree.sync()

    async def __load(self) -> None:
        """
        Initializes the cogs, handlers, and slash cogs that the bot will use. Any files
        that are extensions must have a class that inherits from commands.Cog, which must
        be instantiated in a `setup` function.
        """
        for module in self._extension_filepaths:
            await self.load_extension(module)