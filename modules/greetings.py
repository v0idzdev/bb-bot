import discord.ext.commands as commands
import discord

# |---------- EVENTS ----------|

async def on_member_join(member: discord.Member):
    """Sends a welcome message when a member joins a server.

    :param: member (Member): The member that joined the server.
    """
    channel = member.guild.system_channel

    if channel is not None:
        await channel.send(f':wave: Welcome, {member.mention}.')


async def on_member_remove(member: discord.Member):
    """Sends a welcome message when a member leaves a server.

    :param: member (Member): The member that left the server.
    """
    channel = member.guild.system_channel

    if channel is None:
        await channel.send(f':wave: Goodbye, {member.mention}.')

# |---- REGISTERING MODULE ----|