import discord
from discord import ui


class ClearMessagesView(ui.View):
    """
    Yes/no buttons for clearing all messages in a channel.
    """
    def __init__(self, timeout=120):
        super().__init__(timeout=timeout)
        self.value = None

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