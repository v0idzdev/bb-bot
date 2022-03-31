"""
Contains commands relating to administrator tasks.
"""

import asyncio

import discord
from discord.ext import commands
from utils.buttons import BlacklistClearButton, BlacklistRemoveView, ClearMessagesView, DropdownView
from utils.functions import lift_ban, sanction

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
            return await ctx.send(f"🛠️ Deleted **{amount}** messages.")

        embed = discord.Embed(
            title="⚠️ You have not selected a number of messages to clear.",
            description="❓ Would you like to clear all messages in this channel?",
        )

        view = ClearMessagesView(ctx)
        view.message = await ctx.send(embed=embed, view=view)

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
    async def blacklist(self, ctx: commands.Context, *, words: str=None):
        """
        ⚙️ Bans words from being used.

        Usage:
        ```
        ~blacklist | ~bladd <...words>
        ```
        """
        if not words:
            view = DropdownView(ctx)
            embed = discord.Embed(
                title="🛠️ Please enter one or more words to blacklist."
            )
            view.message = await ctx.send(embed=embed, view=view)
            return

        id = str(ctx.guild.id)
        words = [word.lower() for word in words.split(" ")]

        blacklist = self.client.cache.blacklist
        if id not in blacklist.keys():
            blacklist[id] = []

        # Remove words that are already in the blacklist from the words to add.
        # Make a copy so we can add a footer if any words were removed
        words_ = set(words) - set(blacklist[id])

        # If the list of words is zero, we know that none of the words
        # can be added. So, send an error message
        if not words_:
            return await ctx.send(
                f"❌ {ctx.author.mention}: Sorry. Those words are already in the blacklist."
            )

        # If duplicate words have been removed, add non-duplicates
        # to the list without any error message
        for word in words_:
            blacklist[id].append(word)

        self.client.update_json(FILEPATH, blacklist)

        embed = discord.Embed(
            title=f"🛠️ Words successfully added.",
            description=" ".join(f"`{word}`" for word in words_),
        )

        if len(words) != len(words_):
            embed.set_footer(text="⚠️ Some words were duplicates and were not added.")

        await ctx.send(embed=embed)

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
        id = str(ctx.guild.id)
        blacklist = self.client.cache.blacklist
        mention = ctx.author.mention

        if id not in blacklist.keys():
            return await ctx.send(
                f"❌ {mention}: This server does not have any words blacklisted."
            )

        embed = discord.Embed(
            title=f"⚠️ Are you sure you'd like to clear your server's blacklist?\n",
            description=f"❗ This action cannot be undone.",
        )

        view = BlacklistClearButton(ctx, data=blacklist)
        view.message = await ctx.send(embed=embed, view=view)

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
        blacklist = self.client.cache.blacklist
        server_id = str(ctx.guild.id)

        if server_id not in blacklist.keys():
            return await ctx.send(
                f"❌ {ctx.author.mention}: This server does not have any words blacklisted."
            )

        embed = discord.Embed(title="⛔ Blacklist:")
        embed.description = "".join([f" `{word}` " for word in blacklist[server_id]])

        await ctx.send(embed=embed)

    @commands.command(aliases=["blrem"])
    @commands.has_permissions(manage_messages=True)
    async def blacklistremove(self, ctx: commands.Context, *, words: str=None):
        """
        ⚙️ Removes a word from the list of banned words.

        Usage:
        ```
        ~blacklistremove | ~blrem <...words>
        ```
        """
        if not words:
            view = BlacklistRemoveView(ctx)
            embed = discord.Embed(
                title="🛠️ Please enter one or more words to remove from the blacklist."
            )

            view.message = await ctx.send(embed=embed, view=view)
            return

        id = str(ctx.guild.id)
        words = {word.lower() for word in words.split(" ")}

        blacklist = self.client.cache.blacklist

        if id not in blacklist.keys():
            return await ctx.send(
                f"❌ {ctx.author.mention}: This server does not have any words blacklisted."
            )

        # Only remove words that are already in the blacklist from the words to remove.
        # Make a copy so we can add a footer if any words were removed
        words_ = words & set(blacklist[id])

        if not words_:
            return await ctx.send(
                f"❌ {ctx.author.mention}: Sorry. Those words are not in the blacklist."
            )

        # If duplicate words have been removed, remove non-duplicates
        # from the list without any error message
        for word in words_:
            blacklist[id].remove(word)

        self.client.update_json(FILEPATH, blacklist)

        embed = discord.Embed(
            title=f"🛠️ Words successfully removed.",
            description=" ".join(f"`{word}`" for word in words_),
        )

        if len(words) != len(words_):
            embed.set_footer(
                text="⚠️ Some words were not in the blacklist, and were not removed."
            )

        await ctx.send(embed=embed)


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
