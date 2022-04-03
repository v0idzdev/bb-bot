import discord

from discord.ext import commands
from typing import Optional


class BlacklistClearButton(discord.ui.View):
    def __init__(
        self, ctx: commands.Context, *, data: dict, timeout: Optional[float] = 180
    ):
        super().__init__(timeout=timeout)
        self.blacklist = data
        self.ctx = ctx

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

    async def disable_all_buttons(self, interaction: discord.Interaction = None):
        """
        Disables all buttons.
        """
        interaction = interaction or self

        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def yes(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the yes button.
        """
        await interaction.response.defer()  # manually defer interaction for an increased respond time

        server_id = str(interaction.guild.id)
        server = self.blacklist.get(server_id)

        if server:
            del self.blacklist[server_id]

            interaction.client.update_json("./files/blacklist.json", self.blacklist)
            embed = discord.Embed(title="🛠️ Blacklist Successfully Deleted")

            await interaction.followup.send(embed=embed)
            await self.disable_all_buttons(interaction)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def no(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the no button.
        """
        mention = interaction.user.mention

        await interaction.response.send_message(f":thumbsup: Ok!", ephemeral=True)
        await self.disable_all_buttons(interaction)
