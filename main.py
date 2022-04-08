import asyncio
import itertools
import json
import os
import discord
import dotenv

from discord.ext import commands
from client import Client, get_prefix

dotenv.load_dotenv(".env")

with open("config.json", "r") as file:
    config = json.load(file)

    EXTENSION_PATHS = config["extension_paths"]
    HANDLER_PATHS = config["handler_paths"]
    DATABASE_PATHS = config["database_paths"]

# Change TEST_GUILD_ID to your guild in ./.env if you're working on BB.Bot's development
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))

intents = discord.Intents.all()
status = itertools.cycle(["❓ ~help", "🎵 ~play", "📢 ~twitch"])
client = Client(
    status,
    EXTENSION_PATHS,
    HANDLER_PATHS,
    DATABASE_PATHS,
    TEST_GUILD_ID,
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
)

# Load the client, sync slash commands and start an aiohttp session
async def main():
    """
    Entry point of the application.
    """
    async with client:
        await client.load()

        client.loop.create_task(client.sync())

        TOKEN = os.getenv("TOKEN")
        await client.start(TOKEN)


asyncio.run(main())
