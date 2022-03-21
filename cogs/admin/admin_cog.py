"""
Contains commands relating to administrator tasks.
"""

import nextcord
import asyncio
import json

from nextcord.ext import commands
from .admin_utils import *

FILEPATH = 'files/blacklist.json'


class AdminCog(commands.Cog, name='Admin'):
    """⚙️ Commands for server administrators or moderators."""
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
        if amount is not None: # If the user selected an amount, clear that amount of messages
            await ctx.send(embed=nextcord.Embed(title=f'🛠️ Deleting **{amount}** messages.'))
            return await ctx.channel.purge(limit=amount)

        # Else, create two buttons
        # Then ask the user if they would like to clear all messages in the channel
        yes_button = nextcord.ui.Button(label='Yes', style=nextcord.ButtonStyle.green)
        no_button = nextcord.ui.Button(label='No', style=nextcord.ButtonStyle.red)

        yes_button.callback = lambda interaction: \
            (await interaction.channel.purge(limit=None) for _ in '_').__anext__()
        no_button.callback = lambda interaction: \
            (await interaction.message.delete() for _ in '_').__anext__()

        view = nextcord.ui.View()
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
    async def kick(self, ctx: commands.Context, member: nextcord.Member, *, reason=None):
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
    async def ban(self, ctx: commands.Context, member: nextcord.Member, *, reason=None):
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
    async def softban(self, ctx: commands.Context, member: nextcord.Member, days=1, reason=None):
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
    async def unban(self, ctx: commands.Context, user: nextcord.User):
        """
        ⚙️ Unbans a member from a server.

        Usage:
        ```
        ~unban <user>
        ```
        """
        await lift_ban(ctx, "permanent", user)

    @commands.command(aliases=['bladd'])
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

        with open(FILEPATH, 'r') as file:
            blacklist: dict = json.load(file)

        if id not in blacklist.keys():
            blacklist[id] = []

        if word in blacklist[id]:
            return await ctx.send(f':x: The word \'{word}\' has already been blacklisted.')

        blacklist[id].append(word)
        print(blacklist)

        with open(FILEPATH, 'w') as file:
            json.dump(blacklist, file, indent=4)

        await ctx.send(f':tools: \'{word}\' has been added to the blacklist.')

    @commands.command(aliases=['blclear'])
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

        with open(FILEPATH) as file:
            blacklist: dict = json.load(file)

        mention = ctx.author.mention

        if id not in blacklist.keys():
            return await ctx.send(f':x: {mention}: This server does not have any words blacklisted.')

        yes_button = nextcord.ui.Button(label='Yes', style=nextcord.ButtonStyle.green, emoji='👍🏻')
        no_button = nextcord.ui.Button(label='No', style=nextcord.ButtonStyle.red, emoji='👎🏻')

        async def yes(interaction: nextcord.Interaction):
            for server_id in blacklist.keys():
                if server_id == id:
                    del blacklist[server_id]

                    with open(FILEPATH, 'w') as file:
                        json.dump(blacklist, file, indent=4)

                    return await interaction.message.channel.send(f':thumbsup: {mention}: The blacklist for this server'
                        + f' has successfully been deleted.')

        yes_button.callback = yes

        async def no(interaction: nextcord.Interaction):
            return await interaction.message.channel.send(f':thumbsup: {mention}: Ok!')

        no_button.callback = no

        view = nextcord.ui.View()
        view.add_item(yes_button)
        view.add_item(no_button)

        await ctx.send(
            f':warning: {mention}: Are you sure you\'d like to clear your server\'s blacklist?\n'
            + f'This action cannot be undone.',
            view=view
        )

    @commands.command(aliases=['blshow'])
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
            return await ctx.send(f':x: {ctx.author.mention}: This server does not have any words blacklisted.')

        embed = nextcord.Embed(title='⛔ Blacklist')
        embed.description = ''.join([f' `{word}` ' for word in blacklist[server_id]])

        await ctx.send(embed=embed)

    @commands.command(aliases=['blrem'])
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

        with open(FILEPATH, 'r') as file:
            blacklist: dict = json.load(file)

        if id not in blacklist.keys():
            return await ctx.send(f':x: {ctx.author.mention}: This server does not have any words blacklisted.')

        if word not in blacklist[id]:
            return await ctx.send(f':x: {ctx.author.mention}: That word is not in this server\'s blacklist.')

        blacklist[id].remove(word)
        print(blacklist)

        with open(FILEPATH, 'w') as file:
            json.dump(blacklist, file, indent=4)

        await ctx.send(f':tools: \'{word}\' has been removed from the blacklist.')



def setup(client: commands.Bot):
    client.add_cog(AdminCog(client))


def teardown(client: commands.Bot):
    client.remove_cog(AdminCog(client))

