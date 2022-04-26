"""
Module `__main__` is the main entry point of the application.
This is where the Discord Client is created, setup and run.
"""
__author__ = "Matthew Flegg"
__version__ = "v2.0.0-alpha.1"

import asyncio
import twitchio
import os
import dotenv
import discord
import toml

from core.utils import aliases
from core import DiscordClient
from typing import Dict


async def main():
    """
    This is the main entry point of the application. This is where
    filepaths are loaded, environment variables and retrieved from
    a .env file, and start_application is called.
    """
    dotenv.load_dotenv(".env")

    with open(".setup.toml", "r") as setup, open(".secrets.toml", "r") as secrets:
        theme, \
        guilds, \
        status, \
        extensions = toml.load(setup, _dict=dict).values()
    
        token, \
        twitch_id, \
        twitch_secret,\
        mongo_url = toml.load(secrets, _dict=dict).values()

    mongo_client = aliases.MongoClient(mongo_url)
    twitch_client = twitchio.Client.from_client_credentials(twitch_id, twitch_secret)

    kwargs = {
        "command_prefix": '~',
        "help_command": None,
        "intents": discord.Intents.all(),
    }

    await DiscordClient(
        status,
        theme,
        extensions,
        guilds,
        mongo_client,
        twitch_client,
        **kwargs
    ) \
        .start_pipeline(token)


if __name__ == "__main__":
    asyncio.run(main())