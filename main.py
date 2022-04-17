"""
Module `__main__` is the main entry point of the application.
This is where the Discord Client is created, setup and run.
"""
__author__ = "Matthew Flegg"
__version__ = "v2.0.0-alpha.1"

import asyncio
import itertools
import json
import os
import dotenv
import discord

from core import (
    DiscordClient,
    DiscordClientFactory
)


async def start_application(client: DiscordClient):
    """
    This function starts the application by calling the relevant
    methods of a `Client` instance.

    Params:
     - client (Client): The Discord client to start.
    """
    async with client:
        await client.load()
        client.loop.create_task(client.sync())

        TOKEN = os.getenv("TOKEN")
        await client.start(TOKEN)


def main():
    """
    This is the main entry point of the application. This is where
    filepaths are loaded, environment variables and retrieved from
    a .env file, and start_application is called.
    """
    dotenv.load_dotenv(".env")

    with open("config.json", "r") as config:
        extension_filepaths, handler_filepaths = json.load(config).values()

    testing_guild_ids = [953054451999072276]
    twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
    twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    mongo_connection_url = os.getenv("MONGO_CONNECTION_URL")

    intents = discord.Intents.all()
    status = itertools.cycle(["/"])

    client_factory = DiscordClientFactory()
    client = client_factory.create_discord_client(
        status,
        extension_filepaths,
        handler_filepaths,
        testing_guild_ids,
        mongo_connection_url,
        twitch_client_id,
        twitch_client_secret,
        command_prefix='~',
        intents=intents
    )

    asyncio.run(start_application(client))


if __name__ == "__main__":
    main()