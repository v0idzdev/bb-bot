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

modules = ['admin']
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


@client.event
async def on_member_join(member: discord.Member):
    """Sends a welcome message when a member joins a server.

    :param: member (Member): The member that joined the server.
    """
    channel = member.guild.system_channel

    if channel is not None:
        await channel.send(f':wave: Welcome, {member.mention}.')


@client.event
async def on_member_remove(member: discord.Member):
    """Sends a welcome message when a member leaves a server.

    :param: member (Member): The member that left the server.
    """
    channel = member.guild.system_channel

    if channel is None:
        await channel.send(f':wave: Goodbye, {member.mention}.')

# |---------- LAUNCH ----------|

token = os.getenv('TOKEN')
client.run(token)