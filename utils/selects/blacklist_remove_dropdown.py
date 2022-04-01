import discord
from discord.ext import commands


class BlacklistRemoveDropdown(discord.ui.Select):
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx

        options = [discord.SelectOption(label="\u200b", default=False)]
        self.words = []

        super().__init__(
            placeholder="📃 Choose words to remove from the blacklist...",
            min_values=1,
            max_values=len(options),
            options=options
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Prevents users who weren't the command sender from using buttons.
        """
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            await interaction.response.send_message(
                f"❌ {interaction.user.mention}: This isn't your interaction!",
                ephemeral=True,
            )
            return False

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not self.values:
            return await interaction.followup.send(
                f"❌ {interaction.user.mention}: You need to select one or more than one words to remove from the blacklist!",
                ephemeral=True,
            )

        self.words = self.values
        return