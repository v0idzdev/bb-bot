"""
Contains commands relating to administrator tasks.
"""

import asyncio
import json
import discord

from discord.ext import commands
from .admin_utils import *
from ..admin.admin_components.clear_messages_view import ClearMessagesView
from ..admin.admin_components.clear_blacklist_view import ClearBlacklistView

FILEPATH = "files/blacklist.json"


class AdminCog(commands.Cog, name="Admin"):
    """
    ⚙️ Commands for server administrators or moderators.
    """

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def clear(self, ctx: commands.Context, amount: int | None):
        """
        ⚙️ Clears messages from a text channel.

        Usage:
        ```
        ~clear [amount]
        ```
        """
        if isinstance(amount, int) and amount is not None:
            await ctx.channel.purge(limit=amount)
            return await ctx.send(f'🛠️ Deleted **{amount}** messages.')

        embed = discord.Embed(
            title='⚠️ You have not selected a number of messages to clear.',
            description='❓ Would you like to clear all messages in this channel?',
        )

        return await ctx.send(embed=embed, view=ClearMessagesView(ctx))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        """
        ⚙️ Kicks a member from a server.

        Usage:
        ```
        ~kick <member> [reason]
        ```
        """
        await sanction(ctx, "kick", member, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        """
        ⚙️ Bans a member from a server.

        Usage:
        ```
        ~ban <member> [reason]
        ```
        """
        await sanction(ctx, "ban", member, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def softban(
        self, ctx: commands.Context, member: discord.Member, days=1, reason=None
    ):
        """
        ⚙️ Temporarily bans a member from a server.

        Usage:
        ```
        ~softban <member> [days] [reason]
        ```
        """
        await sanction(ctx, "softban", member, reason=reason)
        await asyncio.sleep(days * 86400)  # Convert to seconds
        await lift_ban(ctx, "temporary", member)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unban(self, ctx: commands.Context, user: discord.User):
        """
        ⚙️ Unbans a member from a server.

        Usage:
        ```
        ~unban <user>
        ```
        """
        await lift_ban(ctx, "permanent", user)

    @commands.command(aliases=["bladd"])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def blacklist(self, ctx: commands.Context, *, word: str):
        """
        ⚙️ Bans a word from being used.

        Usage:
        ```
        ~blacklist | ~bladd <word>
        ```
        """
        id = str(ctx.guild.id)
        word = word.lower()

        with open(FILEPATH, "r") as file:
            blacklist: dict = json.load(file)

        if id not in blacklist.keys():
            blacklist[id] = []

        if word in blacklist[id]:
            return await ctx.send(
                f":x: The word '{word}' has already been blacklisted."
            )

        blacklist[id].append(word)
        print(blacklist)

        with open(FILEPATH, "w") as file:
            json.dump(blacklist, file, indent=4)

        await ctx.send(f":tools: '{word}' has been added to the blacklist.")

    @commands.command(aliases=["blclear"])
    @commands.has_permissions(manage_messages=True)
    async def clearblacklist(self, ctx: commands.Context):
        """
        ⚙️ Clears the list of banned words.

        Usage:
        ```
        ~clearblacklist | ~blclear <word>
        ```
        """
        with open(FILEPATH) as file:
            blacklist: dict = json.load(file)

        id = str(ctx.guild.id) # Server ID to clear the blacklist of

        if id not in blacklist.keys():
            return await ctx.send(
                f"❌ {ctx.author.mention}: This server does not have any words blacklisted."
            )

        embed = discord.Embed(
            title='⚠️ Are you sure you\'d like to clear your server\'s blacklist?.',
            description='❗ This action cannot be undone.',
        )

        await ctx.send(embed=embed, view=ClearBlacklistView(ctx, FILEPATH, blacklist, id))

    @commands.command(aliases=["blshow"])
    @commands.has_permissions(manage_messages=True)
    async def showblacklist(self, ctx: commands.Context):
        """
        ⚙️ Shows the list of banned words.

        Usage:
        ```
        ~showblacklist | ~blshow
        ```
        """
        with open(FILEPATH) as file:
            blacklist: dict = json.load(file)

        server_id = str(ctx.guild.id)
        if server_id not in blacklist.keys():
            return await ctx.send(
                f":x: {ctx.author.mention}: This server does not have any words blacklisted."
            )

        embed = discord.Embed(title="⛔ Blacklist")
        embed.description = "".join([f" `{word}` " for word in blacklist[server_id]])

        await ctx.send(embed=embed)

    @commands.command(aliases=["blrem"])
    @commands.has_permissions(manage_messages=True)
    async def blacklistremove(self, ctx: commands.Context, *, word: str):
        """
        ⚙️ Removes a word from the list of banned words.

        Usage:
        ```
        ~blacklistremove | ~blrem <word>
        ```
        """
        id = str(ctx.guild.id)
        word = word.lower()

        with open(FILEPATH, "r") as file:
            blacklist: dict = json.load(file)

        if id not in blacklist.keys():
            return await ctx.send(
                f":x: {ctx.author.mention}: This server does not have any words blacklisted."
            )

        if word not in blacklist[id]:
            return await ctx.send(
                f":x: {ctx.author.mention}: That word is not in this server's blacklist."
            )

        blacklist[id].remove(word)
        print(blacklist)

        with open(FILEPATH, "w") as file:
            json.dump(blacklist, file, indent=4)

        await ctx.send(f":tools: '{word}' has been removed from the blacklist.")


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(AdminCog(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(AdminCog(client))
