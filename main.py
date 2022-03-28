"""
Main entry point for the application.

This is where the bot is configured and launched.
"""

import asyncio
import itertools
import json
import os

import aiohttp
import discord
import dotenv
from discord.ext import commands

from utils.models import Cache, Twitch


def get_prefix(bot, message: discord.Message):
    """
    Returns the client's command prefix.
    """
    return "~"


class BeepBoop(commands.Bot):
    """
    Contains the client.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.theme = 0x486572 --- Commented this out to add it again later, possibly
        self.possible_status = itertools.cycle(["❓ ~help", "🎵 ~play", "📢 ~twitch"])
        self.session: aiohttp.ClientSession = None
        self.cache: Cache = None
        self.twitch: Twitch = None
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.fill_cache()

    def update_json(self, filename, payload):
        """
        Updates a JSON file.
        """
        with open(filename, 'w') as file:
            json.dump(payload, file, indent=4)

    def fill_cache(self):
        """
        Loads the cache from the blacklist and reaction role json files.
        """
        files = ["./files/blacklist.json", "./files/reactionroles.json"]
        temp_cache = {}

        for file in files:
            with open(file, 'r') as f:
                key = file.split('/')[-1].split('.')[0]
                temp_cache[key] = json.load(f)

        self.cache = Cache(**temp_cache)

    async def start(self, *args, **kwargs) -> None:
        """
        Overriding Bot.startup to create a re-usable aiohttp session.
        """
        async with aiohttp.ClientSession() as self.session:
            self.twitch = Twitch(client_id=self.twitch_client_id, client_secret=self.twitch_client_secret)
            return await super().start(*args, **kwargs)

    async def sync_slash_commands(self):
        """
        Syncs all application commands with Discord.
        """
        print("[SLASH] Syncing slash commands.")
        await self.wait_until_ready()

        # Syncs with all guilds within an hour
        await self.tree.sync()

        # Syncs with test guilds instantly
        TEST_GUILD_ID = int(os.getenv('TEST_GUILD_ID'))
        await self.tree.sync(guild=discord.Object(id=TEST_GUILD_ID))

        print("[SLASH] Finished syncing slash commands")

    async def load_cogs(self):
        """
        Initializes the cogs that the bot uses.
        """
        cogs = [
            "cogs.admin.admin_cog",
            "cogs.help.help_cog",
            "cogs.misc.misc_cog",
            "cogs.music.music_cog",
            "cogs.role.role_cog",
        ]

        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"[COG] Loaded {cog} successfully.")
            except Exception as ex: # Catching a generic exception so we can access the args and __traceback__ properties
                print(f"[COG] {cog} encountered an error.", ex.args, ex.__traceback__)

    async def load_slash_cogs(self):
        """
        Initializes the slash commands.
        """
        commands = [
            "slash_cogs.misc.misc_cog",
        ]

        for command in commands:
            try:
                await self.load_extension(command)
                print(f"[SLASH] Loaded {command} successfully.")
            except Exception as ex:
                print(f"[SLASH] {command} encountered an error.", ex.args, ex.__traceback__)

    async def load_handlers(self):
        """
        Initializes the error, event and task handlers.
        """
        handlers = [
            "handlers.error_handler",
            "handlers.event_handler",
            "handlers.task_handler",
        ]

        for handler in handlers:
            try:
                await client.load_extension(handler)
                print(f"[HANDLER] Loaded {handler} successfully.")
            except Exception as ex:
                print(f"[HANDLER] {handler} encountered an error.", ex.args, ex.__traceback__)


dotenv.load_dotenv(".env")

intents = discord.Intents.all()
client = BeepBoop(command_prefix=get_prefix, intents=intents, case_insensitive=True)

# THIS WAS FOR TESTING PURPOSES ONLY
# @client.tree.command(description="People really like this command!")
# async def nice(interaction: discord.Interaction):
#     await interaction.response.send_message("Haha, cool indeed!")

async def main():
    """
    Main entry point of the application.
    """
    async with client:
        await client.load_cogs()
        await client.load_slash_cogs() # can test this maybe
        await client.load_handlers()

        client.loop.create_task(client.sync_slash_commands())

        TOKEN = os.getenv("TOKEN")
        await client.start(TOKEN)


asyncio.run(main())
