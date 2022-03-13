"""
Contains commands relating to administrator tasks.
"""

import discord.ext.commands as commands
import helpers
import asyncio
import discord
import json


# |---------- COMMANDS ----------|


@commands.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, amount: int):
    """
    Clears messages from a text channel.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    amount (int):
        The number of messages to clear.
    """
    await ctx.channel.purge(limit=amount)


@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason=None):
    """
    Kicks a specified member from a server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    member (Member):
        The member to kick from the server.

    reason (str, optional):
        The reason for the kick.
    """
    await helpers.sanction(ctx, "kick", member, reason=reason)


@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason=None):
    """
    Bans a specified member from a server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    member (Member):
        The member to ban from the server.

    reason (str, optional):
        The reason for the ban.
    """
    await helpers.sanction(ctx, "ban", member, reason=reason)


@commands.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx: commands.Context, member: discord.Member, days=1, reason=None):
    """
    Temporarily bans a specified member from a server.

    The default number of days for a temporary ban is 1.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    member (Member):
        The member to ban from the server.

    reason (str, optional):
        The reason for the ban.
    """
    await helpers.sanction(ctx, "softban", member, reason=reason)
    await asyncio.sleep(days * 86400)  # Convert to seconds
    await helpers.lift_ban(ctx, "temporary", member)


@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx: commands.Context, user: discord.User):
    """
    Unbans a specified user from a server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    user (User):
        The user to unban from the server.
    """
    await helpers.lift_ban(ctx, "permanent", user)


@commands.command()
@commands.has_permissions(manage_messages=True)
async def blacklist(ctx: commands.Context, *, word: str):
    """
    Adds a word to a list of disallowed words in a server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    word (str):
        The word to add to the blacklist.
    """
    filepath = 'files/blacklist.json'
    id = str(ctx.guild.id)

    with open(filepath, "r") as file:
        blacklist: dict = json.load(file)

    if id not in blacklist.keys():
        blacklist[id] = []

    if word in blacklist[id]:
        return await ctx.send(f':x: The word \'{word}\' has already been blacklisted.')

    blacklist[id].append(word)
    print(blacklist)

    with open(filepath, 'w') as file:
        json.dump(blacklist, file, indent=4)
        await ctx.send(f':tools: \'{word}\' has been added to the blacklist.')


# |----- REGISTERING MODULE -----|


def setup(client: commands.Bot):
    """
    Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    helpers.add_commands(client, clear, kick, ban, softban, unban, blacklist)
