"""
Contains commands relating to administrator tasks.
"""

import discord.ext.commands as commands
import discord
import helpers

# |------ USEFUL FUNCTIONS ------|

async def sanction(ctx: commands.Context, punishment: str, member: discord.Member, reason=None):
    """Utility function that bans or kicks a member.

    :param: ctx (Context): Command invocation context.
    :param: punishment (str): Either 'kick'/'ban' depending on the sanction.
    :param: reason (str | None): The reason for the kick/ban.
    """
    if punishment == 'kick':
        await member.kick()
        action = 'kicked'

    if punishment == 'ban':
        await member.ban()
        action = 'banned'

    message_server = f':tools: **{ctx.author.name}** was {action}'
    message_member = f':x: You were {action} from **{ctx.guild.name}**'

    for message in (message_server, message_member):
        message += '.' if reason is None else f' for **{reason}**.'

    await ctx.send(message_server)
    await member.send(message_member)

# |---------- COMMANDS ----------|

@commands.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, amount: int):
    """Clears messages from a text channel.

    :param: ctx (Context): Command invocation context.
    :param: amount (int): The number of messages to clear.
    """
    await ctx.channel.purge(limit=amount)


@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason=None):
    """Kicks a specified member from a server.

    :param: ctx (Context): Command invocation context.
    :param: member (Member): The member to kick from the server.
    :param: reason (str, optional): The reason for the kick.
    """
    await sanction(ctx, 'kick', member, reason=reason)


@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason=None):
    """Kicks a specified member from a server.

    :param: ctx (Context): Command invocation context.
    :param: member (Member): The member to ban from the server.
    :param: reason (str, optional): The reason for the ban.
    """
    sanction(ctx, 'ban', member, reason=reason)


@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx: commands.Context, user: discord.User):
    """Unbans a specified user from a server.

    :param: ctx (Context): Command invocation context.
    :param: user (User): The user to unban from the server.
    """
    message = f':tools: {ctx.author.mention}: {user.name} was unbanned.'

    await ctx.guild.unban(user)
    await ctx.send(message)

# |----- REGISTERING MODULE -----|

def setup(client: commands.Bot):
    """Registers the functions in this module with the client.

    :param: client (Bot): Client instance, to add the commands to.
    """
    helpers.add_commands(clear, kick, ban, client)

