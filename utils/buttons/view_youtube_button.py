import discord

from discord.ext import commands
from discord import ui


class ViewYoutubeButton(ui.View):
    """
    Allows users to choose to view a video in Discord.
    """

    def __init__(
        self, url: str, ctx: commands.Context | discord.Interaction, *, timeout=None
    ):
        super().__init__(timeout=timeout)
        self.url = url

        # This is the user who used the command
        #
        # This view is used in a prefix and slash command, so we want to determine
        # whether we use ctx.author or interaction.user
        self.command_user_id = (
            ctx.author.id if isinstance(ctx, commands.Context) else ctx.user.id
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Prevents users who weren't the command sender from using buttons.
        """
        if interaction.user.id == self.command_user_id:
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

    @ui.button(label="View In Discord", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def view_in_discord(
        self, interaction: discord.Interaction, _: discord.Button
    ):
        """
        Sends a viewable video embed to a user.
        """
        await interaction.response.send_message(f"➡️ {self.url}")
        await self.disable_all_buttons(interaction)

    @ui.button(label="Close", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def close(self, interaction: discord.Interaction, _: discord.Button):
        """
        Deletes the view.
        """
        await self.message.delete()

        # await interaction.response.send_message("👍🏻 Ok!", ephemeral=True)
        # await self.disable_all_buttons(interaction)
