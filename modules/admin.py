"""
Contains commands relating to administrator tasks.
"""

import black
import discord.ext.commands as commands
import discord.ui as UI
import helpers
import asyncio
import discord
import json


# |---------- COMMANDS ----------|


@commands.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def clear(ctx: commands.Context, amount: int | None):
    """
    Clears messages from a text channel.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    amount (int):
        The number of messages to clear.
    """
    if amount is not None: # If the user selected an amount, clear that amount of messages
        await ctx.send(embed=discord.Embed(title=f'🛠️ Deleting **{amount}** messages.'))
        return await ctx.channel.purge(limit=amount)

    # Else, create two buttons
    # Then ask the user if they would like to clear all messages in the channel
    yes_button = UI.Button(label='Yes', style=discord.ButtonStyle.green)
    no_button = UI.Button(label='No', style=discord.ButtonStyle.red)

    yes_button.callback = lambda interaction: \
        (await interaction.channel.purge(limit=None) for _ in '_').__anext__()
    no_button.callback = lambda interaction: \
        (await interaction.message.delete() for _ in '_').__anext__()

    view = UI.View()
    view.add_item(yes_button)
    view.add_item(no_button)

    return await ctx.send(
        f':warning: {ctx.author.mention}: You have not selected a number of messages to clear.\n'
        + 'Would you like to clear all messages in this channel?',
        view=view
    )


@commands.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 30, commands.BucketType.user)
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
@commands.cooldown(1, 30, commands.BucketType.user)
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
@commands.cooldown(1, 30, commands.BucketType.user)
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
@commands.cooldown(1, 2, commands.BucketType.user)
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


@commands.command(aliases=['bladd'])
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 2, commands.BucketType.user)
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
    word = word.lower()

    with open(filepath, 'r') as file:
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


@commands.command(aliases=['blclear'])
@commands.has_permissions(manage_messages=True)
async def clearblacklist(ctx: commands.Context):
    """
    Clears the blacklist for a server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.
    """
    filepath = 'files/blacklist.json'
    id = str(ctx.guild.id)

    with open(filepath) as file:
        blacklist: dict = json.load(file)

    mention = ctx.author.mention

    if id not in blacklist.keys():
        return await ctx.send(f':x: {mention}: This server does not have any words blacklisted.')

    yes_button = UI.Button(label='Yes', style=discord.ButtonStyle.green, emoji='👍🏻')
    no_button = UI.Button(label='No', style=discord.ButtonStyle.red, emoji='👎🏻')

    async def yes(interaction: discord.Interaction):
        for server_id in blacklist.keys():
            if server_id == id:
                del blacklist[server_id]

                with open(filepath, 'w') as file:
                    json.dump(blacklist, file, indent=4)

                return await interaction.message.channel.send(f':thumbsup: {mention}: The blacklist for this server'
                    + f'has successfully been deleted.')

    yes_button.callback = yes

    async def no(interaction: discord.Interaction):
        return await interaction.message.channel.send(f':thumbsup: {mention}: Ok!')

    no_button.callback = no

    view = UI.View()
    view.add_item(yes_button)
    view.add_item(no_button)

    await ctx.send(
        f':warning: {mention}: Are you sure you\'d like to clear your server\'s blacklist?\n'
        + f'This action cannot be undone.',
        view=view
    )


# |----- REGISTERING MODULE -----|


def setup(client: commands.Bot):
    """
    Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    helpers.add_commands(
        client,
        clear,
        kick,
        ban,
        softban,
        unban,
        blacklist,
        clearblacklist
    )
