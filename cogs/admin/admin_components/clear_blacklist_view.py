import discord
import json

from discord import ui
from discord.ext import commands


class ClearBlacklistView(ui.View):
    """
    Yes/no buttons for clearing all blacklisted words in a server.
    """
    def __init__(self, ctx: commands.Context, filepath: str, blacklist, id: str):
        super().__init__()

        self.value = None
        self.ctx = ctx
        self.id = id
        self.filepath = filepath
        self.blacklist = blacklist

    @ui.button(label='👍🏻 Yes', style=discord.ButtonStyle.grey)
    async def yes(self, button: ui.Button, interaction: discord.Interaction):
        """
        Callback for the yes button.
        """
        for server_id in self.blacklist.keys():
            if server_id != id:
                continue

            del self.blacklist[server_id]

            with open(self.filepath, "w") as file:
                json.dump(self.blacklist, file, indent=4)

            return await interaction.message.channel.send(
                f"👍🏻 {interaction.message.author.mention}: The blacklist for this server has successfully been deleted."
            )

        self.stop()

    @ui.button(label='👎🏻 No', style=discord.ButtonStyle.green)
    async def no(self, button: ui.Button, interaction: discord.Interaction):
        """
        Callback for the no button.
        """
        await interaction.message.channel.send(f":thumbsup: {interaction.message.author.mention}: Ok!")
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Only allows the view to be interacted with by its author.
        """
        return interaction.user == self.ctx.author