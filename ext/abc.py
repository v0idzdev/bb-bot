"""
Module `abc` contains abstract base classes for extensions,
handlers, and cogs that implements common functionality.
"""
import discord
import core

from discord.ext import commands
from discord import app_commands


class SlashCommandCog(commands.Cog, app_commands.Group):
    """
    Class `SlashCommandCog` is a base class from which to derive discord.py
    application command cogs.
    """
    def __init__(self, client: core.DiscordClient):
        """
        Returns a SlashCommandCog instance that implements a common constructor
        method. Use this to implement application commands.

        Params:
         - client (core.DiscordClient): The client to use the extension for.

        Returns:
         - An `Extension` instance that can be inherited from by slash cogs.
        """
        self.client = client