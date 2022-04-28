"""
Module `events` contains the `EventHandler` extension,
which is used to respond to discord events.
"""
import discord
import asyncio
import core

from discord.ext import commands


class EventHandler(commands.Cog):
    """
    Class `EventHandler` is responsible for executing code
    in response to various client-side events.
    """
    def __init__(self, client: core.DiscordClient):
        self.client = client
        super().__init__()
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User) -> None:
        """
        This event is triggered when users react to a message
        that the bot has sent.

        This method is responsible for ensuring that users can
        only vote once on a poll.

        Params:
         - reaction (discord.Reaction): The reaction that was added.
         - user (discord.User): The user who added the reaction.
        """
        if user.bot:
            return

        message: discord.Message = discord.utils.find(
            lambda x: x == reaction.message, self.client.cached_messages
        )

        for existing_reaction in message.reactions:
            users = {user async for user in existing_reaction.users()}

            if user in users and str(existing_reaction) != str(reaction):
                await message.remove_reaction(existing_reaction.emoji, user)


async def setup(client: core.DiscordClient) -> None:
    """
    Registers the command group/cog with the discord client.
    All extensions must have a setup function.

    Params:
     - client: (DiscordClient): The client to register the cog with.
    """
    await client.add_cog(EventHandler(client))


async def teardown(client: core.DiscordClient) -> None:
    """
    De-registers the command group/cog with the discord client.
    This is not usually needed, but is useful to have.

    Params:
     - client: (DiscordClient): The client to de-register the cog with.
    """
    await client.remove_cog(EventHandler(client))