"""
Contains commands relating to administrator tasks.
"""

import discord.ext.commands as commands
import modules.helpers as helpers
import asyncio
import start
import discord
import json


# |------ USEFUL FUNCTIONS ------|


async def sanction(
    ctx: commands.Context, punishment: str, member: discord.Member, reason=None
):
    """
    Utility function that bans or kicks a member.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    punishment (str):
        Either 'kick'/'ban' depending on the sanction.

    reason (str | None):
        The reason for the kick/ban.
    """
    match punishment:

        case "ban":
            await member.ban()
            action = "permanently banned"

        case "softban":
            await member.ban()
            action = "temporarily banned"

        case "kick":
            await member.kick()
            action = "kicked"

    message_server = f":tools: **{ctx.author.name}** was {action}"
    message_member = f":x: You were {action} from **{ctx.guild.name}**"

    for message in (message_server, message_member):
        message += "." if reason is None else f" for **{reason}**."

    await ctx.send(message_server)
    await member.send(message_member)


async def lift_ban(ctx: commands.Context, ban_type: str, user: discord.User):
    """
    Utility function that unbans a member.

    Outputs an appropriate message depending on whether the ban
    was permanent or temporary.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    ban_type (str):
        The type of ban that the user had - either 'temporary' or 'permanent'

    reason (str | None):
        The reason for the kick/ban.
    """
    message = f":tools: {ctx.author.mention}: {user.name}'s {ban_type} ban was lifted."

    await ctx.guild.unban(user)
    await ctx.send(message)


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
    await sanction(ctx, "kick", member, reason=reason)


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
    await sanction(ctx, "ban", member, reason=reason)


@commands.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx: commands.Context, member: discord.Member, days=1, reason=None):
    """Temporarily bans a specified member from a server.

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
    await sanction(ctx, "softban", member, reason=reason)
    await asyncio.sleep(days * 86400)  # Convert to seconds
    await lift_ban(ctx, "temporary", member)


@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx: commands.Context, user: discord.User):
    """Unbans a specified user from a server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    user (User):
        The user to unban from the server.
    """
    await lift_ban(ctx, "permanent", user)


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
    filepath = "files/blacklist.json"
    id = str(ctx.guild.id)

    with open(filepath, "r") as file:
        blacklist: dict = json.load(file)

    if id not in blacklist.keys():
        blacklist[id] = []

    if word in blacklist[id]:
        return await ctx.send(f":x: The word '{word}' has already been blacklisted.")

    blacklist[id].append(word)
    print(blacklist)

    with open(filepath, "w") as file:
        json.dump(blacklist, file, indent=4)
        await ctx.send(f":tools: '{word}' has been added to the blacklist.")


# |----------- EVENTS -----------|


async def on_message(message: discord.Message):
    """
    Called when a message is sent.

    Parameters
    ----------

    message (Message):
        The message that was sent.
    """
    with open("files/blacklist.json", "r") as file:
        blacklist = json.load(file)

    id = str(message.guild.id)

    if start.prefix in message.content or id not in blacklist:
        return

    words_msg = set(message.content.split(" "))
    words_ban = set(blacklist.get(id))

    for wordlist in (words_msg, words_ban):  # Convert words in both lists
        wordlist = {word.strip().lower() for word in wordlist}

    if words_msg & words_ban:  # If any banned words are in the message
        await message.delete()


# |----- REGISTERING MODULE -----|


def setup(client: commands.Bot):
    """Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    helpers.add_commands(client, clear, kick, ban, softban, unban, blacklist)
    helpers.add_listeners(client, (on_message, on_message.__name__))
