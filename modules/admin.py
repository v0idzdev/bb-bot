"""
Contains commands relating to administrator tasks.
"""

import asyncio
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
    match punishment:

        case 'kick':
            await member.kick()
            action = 'kicked'

        case 'ban':
            await member.ban()
            action = 'banned'

        case 'softban':
            await member.ban()
            action = 'softban'

    message_server = f':tools: **{ctx.author.name}** was {action}'
    message_member = f':x: You were {action} from **{ctx.guild.name}**'

    for message in (message_server, message_member):
        message += '.' if reason is None else f' for **{reason}**.'

    await ctx.send(message_server)
    await member.send(message_member)


async def lift_ban(ctx: commands.Context, ban_type: str, user: discord.User):
    """Utility function that unbans a member.

    Outputs an appropriate message depending on whether the ban
    was permanent or temporary.

    :param: ctx (Context): Command invocation context.
    :param: ban_type (str): The type of ban that the user had - either 'temporary' or 'permanent'
    :param: reason (str | None): The reason for the kick/ban.
    """
    message = f':tools: {ctx.author.mention}: {user.name}\'s {ban_type} ban was lifted.'

    await ctx.guild.unban(user)
    await ctx.send(message)

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
    """Bans a specified member from a server.

    :param: ctx (Context): Command invocation context.
    :param: member (Member): The member to ban from the server.
    :param: reason (str, optional): The reason for the ban.
    """
    await sanction(ctx, 'ban', member, reason=reason)


@commands.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx: commands.Context, member: discord.Member, days=3, reason=None):
    """Temporarily bans a specified member from a server.

    The default number of days for a temporary ban is 3.

    :param: ctx (Context): Command invocation context.
    :param: member (Member): The member to ban from the server.
    :param: reason (str, optional): The reason for the ban.
    """
    await sanction(ctx, 'softban', member, reason=reason)
    await asyncio.sleep(days * 86400) # Convert to seconds
    await lift_ban(ctx, 'temporary', member)


@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx: commands.Context, user: discord.User):
    """Unbans a specified user from a server.

    :param: ctx (Context): Command invocation context.
    :param: user (User): The user to unban from the server.
    """
    await lift_ban(ctx, 'permanent', user)

# |----- REGISTERING MODULE -----|

def setup(client: commands.Bot):
    """Registers the functions in this module with the client.

    :param: client (Bot): Client instance, to add the commands to.
    """
    helpers.add_commands(clear, kick, ban, client)

