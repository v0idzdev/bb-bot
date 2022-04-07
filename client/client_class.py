import itertools
import json
import os
import aiohttp
import discord

from discord.ext import commands
from utils import Cache, Twitch


class Client(commands.Bot):
    """
    Contains the client that the bot uses.
    """

    def __init__(
        self,
        possible_status: itertools.cycle,
        extension_paths: list[str],
        handler_paths: list[str],
        database_paths: dict[str, str],
        test_guild_id: int = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.possible_status = possible_status
        self.session: aiohttp.ClientSession = None
        self.cache: Cache = None

        self.twitch: Twitch = None
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")

        self._extension_paths = extension_paths
        self._handler_paths = handler_paths
        self._database_paths = database_paths
        self._test_guild_id = test_guild_id

        self._fill_cache()

    @property
    def database_paths(self):
        """
        Returns a dictionary containing the paths to JSON database files.
        """
        return self._database_paths

    def _fill_cache(self) -> None:
        """
        Loads JSON database files and stores their data as a Cache object in self.cache.
        """
        temporary_cache = {}

        for key, filepath in self._database_paths.items():
            with open(filepath, "r") as file:
                temporary_cache[key] = json.load(file)

        self.cache = Cache(**temporary_cache)

    def update_json(self, filename, payload) -> None:
        """
        Updates a modified Cache attribute and stores it in a JSON file.
        """
        with open(filename, "w") as file:
            json.dump(payload, file, indent=4)

    async def start(self, *args, **kwargs) -> None:
        """
        Overrides Bot.startup to create a re-usable aiohttp session.
        """
        async with aiohttp.ClientSession() as self.session:
            self.twitch = Twitch(self.twitch_client_id, self.twitch_client_secret)

            return await super().start(*args, **kwargs)

    async def sync(self) -> None:
        """
        Syncs all application commands with Discord.
        """
        await self.wait_until_ready()

        if self._test_guild_id:
            await self.tree.sync(guild=discord.Object(id=self._test_guild_id))

        await self.tree.sync()

    async def load(self) -> None:
        """
        Initializes the cogs, handlers, and slash cogs that the bot will use.
        """
        for module in self._extension_paths + self._handler_paths:
            await self.load_extension(module)
