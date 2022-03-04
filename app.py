import discord
import logging as log
import os

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv(".env")

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
extensions = ["greetings", "miscellaneous", "admin", "music",
              "help", "chatbot", "error_handler"]

for ext in extensions:
    bot.load_extension(f"extensions.{ext}")

@bot.event
async def on_ready():
    """Displays a series of logs to the screen when the bot has loaded"""

    print(f"Username: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Bot loaded successfully")


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
