"""
start.py is the main entry point of the application.

This script registers the client, loads extensions and
executes an on_ready function.

ENSURE YOU HAVE THE FOLLOWING TO USE THIS CODE:

- ALl privileged gateway intents
- Administrator permissions (for both you and your bot)
- A .env file in the root directory, with: TOKEN=<your_token>

Author: Matthew Flegg ~ matthewflegg@outlook.com
GitHub repo: matthewflegg/beepboop/
Version: 1.X.X (Rewrite)
"""

# Import project dependencies
import discord
import os

from discord.ext import commands, tasks # commands: all the main discord stuff, tasks: background tasks lib
from dotenv import load_dotenv # Lets us use an environment variables file
from itertools import cycle

# Load environment variables
load_dotenv('.env')

# Get intents
# Intents are which things from the discord API the client is allowed to use
intents = discord.Intents.all()
intents.members = True

# Create the client, which is the bot
# The first parameter, '.', is the command prefix: .examplecommand
client = commands.Bot('.', intents=intents)

# Loads all the extensions (a.k.a, cogs) in the 'cogs' folder
try:
    cogs = os.listdir('./cogs') # Gets all the filenames in the 'cogs' directory

    for cog in cogs:
        cog = cog.replace('.py', '') # Remove .py from the file name
        client.load_extension(f'cogs.{cog}')
except:
    pass


@client.event
async def on_ready():
    """
    Called when the bot has loaded.
    """
    print(f'Name: {client.user.name}\nID: {client.user.id}')


# Stores all of the activities that will be displayed on the bot's profile,
# e.g, playing <?help>
activities = cycle([discord.Game('?help'), discord.Game('?play'), discord.Game('?ai')])


@tasks.loop(seconds=30)
async def change_presence():
    """
    Every 30 seconds, change the bot's presence.

    Presences are stored in a cycle, which is a linked list where the last
    element points to the first. You get the next element with item = next(items).
    """
    await client.change_presence(activity=next(activities))


# Get the token from the environment vars file, then run the client
TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
