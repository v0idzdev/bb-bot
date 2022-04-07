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

        self.extension_paths = extension_paths
        self.handler_paths = handler_paths
        self.database_paths = database_paths
        self.test_guild_id = test_guild_id

        self._fill_cache()

    def _fill_cache(self, filepath, data) -> None:
        """
        Loads JSON database files and stores their data as a Cache object in self.cache.
        """
        temporary_cache = {}

        for (key, filepath) in self.database_paths.values():
            with open(filepath, "r") as file:
                temporary_cache[key] = json.load(file)

        self.cache = Cache(**temporary_cache)

    def update_json(self, filename, payload):
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

    async def sync(self):
        """
        Syncs all application commands with Discord.
        """
        await self.wait_until_ready()

        if self.test_guild_id:
            await self.tree.sync(guild=discord.Object(id=self.test_guild_id))

        await self.tree.sync()

    async def load(self):
        """
        Initializes the cogs, handlers, and slash cogs that the bot will use.
        """
        for module in self.extension_paths + self.handler_paths:
            await self.load_extension(module)
