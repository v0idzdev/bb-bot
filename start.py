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

prefix = "~"
status = itertools.cycle(["~help", "~ai", "~play"])
client = commands.Bot(prefix, intents=intents, help_command=None) # Help command = none so we can override it

modules = filter(lambda mod: mod.endswith('.py'), os.listdir('./modules')) # Get all files ending in .py
modules = filter(lambda mod: mod not in ('__init__.py', 'helpers.py'), list(modules)) # Remove __init__ and helpers

for mod in list(modules):
    client.load_extension(f'modules.{mod}'.replace('.py', ''))


# |----- BACKGROUND TASKS -----|


@tasks.loop(seconds=30)
async def change_presence():
    """
    Changes the bot's presence every 30 seconds.
    """
    activity = next(status)
    await client.change_presence(activity=discord.Game(activity))


# |---------- EVENTS ----------|


@client.event
async def on_ready():
    """
    Executes when the bot has loaded.
    """
    print(f"Loaded {client.user.name} successfully.")
    await change_presence.start()


# |---------- LAUNCH ----------|


token = os.getenv("TOKEN")
client.run(token)
