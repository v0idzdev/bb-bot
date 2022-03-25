import discord

from discord import ui
from discord.ext import commands


class ClearMessagesView(ui.View):
    """
    Yes/no buttons for clearing all messages in a channel.
    """
    def __init__(self, ctx: commands.Context):
        super().__init__()

        self.value = None
        self.ctx = ctx

    @ui.button(label='👍🏻 Yes', style=discord.ButtonStyle.grey)
    async def yes(self, button: ui.Button, interaction: discord.Interaction):
        """
        Callback for the yes button.
        """
        await interaction.channel.purge(limit=None)
        self.stop()

    @ui.button(label='👎🏻 No', style=discord.ButtonStyle.green)
    async def no(self, button: ui.Button, interaction: discord.Interaction):
        """
        Callback for the no button.
        """
        await interaction.message.delete()
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Only allows the view to be interacted with by its author.
        """
        return interaction.user == self.ctx.author