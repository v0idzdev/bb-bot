"""
Module `admin_cog` contains the `Admin` cog, which implements
admin commands for BB.Bot.
"""
import discord
import bot

from typing import List, Optional, Any
from discord.ext import commands
from discord import app_commands


class AdminCog(commands.Cog, app_commands.Group, name="admin"):
    """
    ⚙️ Commands for server administrators or moderators.
    """
    def __init__(self, client: bot.Client):
        self.client = client
        super().__init__()

    @app_commands.command()
    @app_commands.describe(amount="❓ The amount of messages to clear.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, *, amount: Optional[int]=None) -> List[discord.Message] | Any | None:
        """
        ⚙️ Clears messages from a text channel.

        Usage:
        ```
        /admin clear [amount]
        ```
        """
        if not amount:
            return await interaction.message.channel.purge(limit=None)

        embed = discord.Embed(
            title="⚠️ You Have Not Selected a Number of Messages to Clear",
            description="❓ Would you like to clear all messages in this channel?",
        )

        view = bot.ClearMessagesView(command_author=interaction.user)
        return await interaction.response.send_message(embed=embed, view=view)


async def setup(client: bot.Client) -> None:
    """
    Creates an instance of the admin cog and registers it with
    the discord client as an extension.

    Params:
     - client (bot.Client): The client to add the cog to.
    """
    await client.add_cog(AdminCog(client))


async def teardown(client: bot.Client) -> None:
    """
    Creates an instance of the admin cog and de-registers it with
    the discord client as an extension.

    Params:
     - client (bot.Client): The client to remove the cog to.
    """
    await client.remove_cog(AdminCog(client))