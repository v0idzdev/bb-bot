import asyncio
import itertools
import json
import os
import discord
import dotenv

from discord.ext import commands
from client import Client, get_prefix

dotenv.load_dotenv(".env")

# Load the paths used for cogs, handlers, and databases
with open("config.json", "r") as file:
    config = json.load(file)

    EXTENSION_PATHS = config["extension_paths"]
    HANDLER_PATHS = config["handler_paths"]
    DATABASE_PATHS = config["database_paths"]

# Change TEST_GUILD_ID to your guild in ./.env if you're working on BB.Bot's development
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))

# Configure intents and statuses, and create a client.client_class.Client() instance
#
# Pass in the cog, handler, and database filepaths as well as
# the command prefix function, intents, and a case insensitivity setting.
# Change these in config.json if you need to.
intents = discord.Intents.all()
status = itertools.cycle(["❓ ~help", "🎵 ~play", "📢 ~twitch"])
client = Client(
    status,
    extension_paths=EXTENSION_PATHS,
    handler_paths=HANDLER_PATHS,
    database_paths=DATABASE_PATHS,
    test_guild_id=TEST_GUILD_ID,
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
