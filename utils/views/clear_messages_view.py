import discord

from discord.ext import commands
from typing import Optional


class ClearMessagesView(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def on_timeout(self) -> None:
        """
        Called when the view times out.
        """
        await self.disable_all_buttons()

    async def disable_all_buttons(self, interaction: discord.Interaction = None):
        """
        Disables all buttons.
        """
        interaction = interaction or self

        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Prevents users who weren't the command sender from using buttons.
        """
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            await interaction.response.send_message(
                ":x: This isn't your interaction!", ephemeral=True
            )
            return False

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def yes(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the yes button.
        """
        await interaction.response.defer()  # manually defer interaction for an increased respond time

        channel_pos = interaction.channel.position
        category = interaction.channel.category
        new_channel = await interaction.channel.clone()

        await new_channel.edit(category=category, position=channel_pos)
        await interaction.channel.delete()

        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def no(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the no button.
        """
        await interaction.response.send_message("👍🏻 Aborting command.", ephemeral=True)
        await self.disable_all_buttons(interaction)
