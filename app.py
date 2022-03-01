import discord
import logging as log
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv(".env")

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
bot.load_extension("extensions.greetings")     # Load greetings commands/events
bot.load_extension("extensions.miscellaneous") # Load misc commands
bot.load_extension("extensions.admin")         # Load admin commands
bot.load_extension("extensions.help")          # Load help commands


@bot.event
async def on_ready():
    """Displays a series of logs to the screen when the bot has loaded.
    Used for debugging purposes.
    """

    log.info(f"Username: {bot.user.name}")
    log.info(f"Bot ID: {bot.user.id}")
    log.info(f"Bot loaded successfully")


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
