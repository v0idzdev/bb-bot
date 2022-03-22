"""
Main entry point for the application.

This is where the bot is configured and launched.
"""

import asyncio
import itertools
import os
import aiohttp
import discord
import dotenv

from discord.ext import commands


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

        self.theme = 0x486572
        self.possible_status = itertools.cycle(["~help", "~play"])
        self.session: aiohttp.ClientSession = None

    async def start(self, *args, **kwargs) -> None:
        """
        Overriding Bot.startup to create a re-usable aiohttp session.
        """
        async with aiohttp.ClientSession() as self.session:
            return await super().start(*args, **kwargs)

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
                print(f"[COG] Loaded <<{cog}>> successfully.")
            except:
                print(f"[COG] <<{cog}>> encountered an error.")

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
                print(f"[HANDLER] Loaded <<{handler}>> successfully.")
            except:
                print(f"[HANDLER] <<{handler}>> encountered an error.")


dotenv.load_dotenv("files/.env")

intents = discord.Intents.all()
client = BeepBoop(command_prefix=get_prefix, intents=intents, case_insensitive=True)


async def main():
    """
    Main entry point of the application.
    """
    await client.load_cogs()
    await client.load_handlers()

    TOKEN = os.getenv("TOKEN")
    await client.start(TOKEN)


asyncio.run(main())
