"""
Main entry point for the application.

This is where the bot is configured and launched.
"""

import nextcord
import os
import itertools
import dotenv

from nextcord.ext import commands, tasks


dotenv.load_dotenv('files/.env')

intents = nextcord.Intents.all()
intents.members = True

prefix = "~"
colour = 0x486572
status = itertools.cycle(['~help', '~play'])
client = commands.Bot(prefix, intents=intents, case_insensitive=True) # Help command = none so we can override it

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
    client.load_extension(cog)
    print(f'[COG] Loaded "{cog}" successfully')

# Doing the same for handlers
# This is separate to improve readability
handlers = [
    'handlers.error_handler',
    'handlers.event_handler',
    'handlers.task_handler'
]

for handler in handlers:
    client.load_extension(handler)
    print(f'[HANDLER] Loaded "{handler}" successfully')


TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
