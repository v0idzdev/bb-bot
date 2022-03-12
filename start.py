"""
Main entry point for the application.

This is where the bot is configured and launched.
"""

import discord
import os
import discord.ext.commands as commands
import discord.ext.tasks as tasks
import itertools

# |---------- CONFIG ----------|

intents = discord.Intents.all()
intents.members = True

prefix = '~'
status = itertools.cycle(['~help', '~ai', '~play'])
client = commands.Bot(prefix, intents=intents)

modules = ['admin', 'greetings']
for module in modules:
    client.load_extension(f'modules.{module}')

# |----- BACKGROUND TASKS -----|

@tasks.loop(seconds=30)
async def change_presence():
    """Changes the bot's presence every 30 seconds."""
    activity = next(status)
    await client.change_presence(activity=discord.Game(activity))

# |---------- EVENTS ----------|

@client.event
async def on_ready():
    """Executes when the bot has loaded."""
    print(f'Loaded {client.user.name} successfully.')
    await change_presence.start()

# |---------- LAUNCH ----------|

token = os.getenv('TOKEN')
client.run(token)