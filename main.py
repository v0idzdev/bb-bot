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
    return "~"

class BeepBoop(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme = 0x486572
        self.possible_status = itertools.cycle(['~help', '~play'])
        self.session: aiohttp.ClientSession = None

    async def start(self, *args, **kwargs) -> None:
        # overriding Bot.startup to create a re-usable aiohttp session
        async with aiohttp.ClientSession() as self.session:
            return await super().start(*args, **kwargs)

    async def load_cogs(self):
        # List of filepaths in the Python import format
        # This is here because a loop isn't necessary
        cogs = [
            'cogs.admin.admin_cog',
            'cogs.help.help_cog',
            'cogs.misc.misc_cog',
            'cogs.music.music_cog',
            'cogs.role.role_cog'
        ]
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f'[COG] Loaded <<{cog}>> successfully.')
            except:
                print(f'[COG] <<{cog}>> encountered an error.')

    async def set_event_hooks(self):
        # Doing the same for handlers
        # This is separate to improve readability
        handlers = [
            'handlers.error_handler',
            'handlers.event_handler',
            'handlers.task_handler'
        ]
        for handler in handlers:
            try:
                await client.load_extension(handler)
                print(f'[HANDLER] Loaded <<{handler}>> successfully.')
            except:
                print(f'[HANDLER] <<{handler}>> encountered an error.')


dotenv.load_dotenv('files/.env')
intents = discord.Intents.all()

client = BeepBoop(
                  command_prefix=get_prefix, 
                  intents=intents, 
                  case_insensitive=True
        )

async def main():
    TOKEN = os.getenv("TOKEN")
    await client.load_cogs()
    await client.set_event_hooks()
    await client.start(TOKEN)

asyncio.run(main())
