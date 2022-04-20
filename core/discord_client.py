"""
Module `discord_client` contains the `DiscordClient` class, which is
responsible for loading extensions, syncing application commands against
the Discord API, and starting the bot.
"""
import aiohttp
import discord
import itertools
import logging
import sys

from core.utils.aliases import MongoClient
from discord.ext import commands
from core.apis import TwitchClient
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
       possible_statuses: itertools.cycle,
       extension_filepaths: List[str],
       testing_guild_ids: List[int],
       twitch_client_id: str,
       twitch_client_secret: str,
       mongo_connection_url: str,
        **kwargs: Dict[str, Any]
    ) -> None:
        """
        Creates an instance of `DiscordClient` that is used to interact with
        Discord, and is responsible for loading & starting the bot, and
        syncing slash commands.

        Params:
         - possible_statuses (itertools.Cycle): A list of statuses the bot will cycle through.
         - extension_filepaths (list[str]): The filepaths of extensions the bot will use.
         - testing_guild_ids (list[int]): The IDs of testing guilds the bot is in.
         - mongo_connection_url (str): The URL used to connect to a MongoDB database.
         - twitch_client_id (str): The Twitch API application's ID.
         - twitch_client_secret (str): The Twitch API application's secret.

        Returns:
         - A `DiscordClient` instance.
        """
        super().__init__(**kwargs)

        self.possible_statuses = possible_statuses
        self.session: aiohttp.ClientSession = None

        # Read-only attributes
        self._extension_filepaths = extension_filepaths
        self._twitch_client: TwitchClient = None
        self._mongo_client: MongoClient = None

        # Strictly private attributes
        self.__testing_guild_ids = testing_guild_ids
        self.__twitch_client_id = twitch_client_id
        self.__twitch_client_secret = twitch_client_secret
        self.__mongo_connection_url = mongo_connection_url

        logging.basicConfig(
            handlers=[logging.StreamHandler(sys.stdout)],
            format="%(levelname)s %(asctime)s - %(message)s", 
            level=logging.INFO
        )

    @property
    def extension_filepaths(self) -> list[str]:
        """
        Returns the value of self._extension_filepaths. This stops the value
        being set from outside the `Client` class.
        """
        return self._extension_filepaths

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
    def twitch_client(self) -> TwitchClient:
        """
        Returns the value of self._twitch_client. This stops the value
        being set from outside the `Client` class.
        """
        return self._twitch_client

    async def start(self, *args, **kwargs) -> None:
        """
        Overrides commands.Bot.start to create a re-usable aiohttp.ClientSession, and to
        create TwitchClient and MongoClient instances. Use this method to start the bot.
        """
        async with aiohttp.ClientSession() as self.__session:
            self._twitch_client = self.__create_twitch_client()
            self._mongo_client = self.__create_mongo_client()

            return await super().start(*args, **kwargs)

    async def sync(self) -> None:
        """
        Synchronizes application commands the bot uses with Discord. For any server/guild
        with an ID in `self.__testing_guild_ids`, slash commands will be synced instantly.
        For all other guilds, this may take up to an hour to complete.
        """
        await self.wait_until_ready()

        for test_guild_id in self.__testing_guild_ids:
            await self.tree.sync(guild=discord.Object(id=test_guild_id))

        await self.tree.sync()

    async def load(self) -> None:
        """
        Initializes the cogs, handlers, and slash cogs that the bot will use. Any files
        that are extensions must have a class that inherits from commands.Cog, which must
        be instantiated in a `setup` function.
        """
        for module in self._extension_filepaths:
            await self.load_extension(module)

    async def __create_twitch_client(self) -> TwitchClient:
        """
        Internal method that returns an instance of TwitchClient.
        """
        return TwitchClient(self.__twitch_client_id, self.__twitch_client_secret)

    async def __create_mongo_client(self) -> MongoClient:
        """
        Internal method that returns an instance of AsyncIOMotorClient.
        """
        return MongoClient(self.__mongo_connection_url)