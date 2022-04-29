"""
Module `youtube_view` contains class `YoutubeView`, which provides
yes and no buttons for viewing a Youtube video in discord when prompted.
"""
import discord

from discord import ui
from typing import Any
from .base_view import BaseView


class YoutubeView(BaseView):
    """
    Class `YoutubeView` provides a set of yes or no buttons when
    a user is asked if they want to view a video in discord.
    """
    def __init__(
        self,
        youtube_url: str,
        interaction: discord.Interaction,
        **kwargs: Any
    ) -> None:
        """
        Creates a `YoutubeView` UI component that allows users to
        view a video in discord, if they choose yes.

        Params:
         - interaction (discord.Interaction): The interaction the command was invoked with.
         - message (discord.Message): Pass the message the view is sent in.
         - **kwargs (Any): Any keyword arguments that `discord.ui.View` accepts.
        """
        super().__init__(interaction, **kwargs)
        self.youtube_url = youtube_url
    
    @ui.button(label="View In Discord", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def view_in_discord(
        self, interaction: discord.Interaction, _: discord.Button
    ) -> None:
        """
        Sends a viewable video embed to a user.

        Params:
         - interaction (discord.Interaction): The button interaction.
        """
        await interaction.response.send_message(f"**[Here's your link!]({self.youtube_url})**")
        await self.disable_all_buttons()

    @ui.button(label="Close", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def close(self, interaction: discord.Interaction, _: discord.Button) -> None:
        """
        Deletes the view. This is done when the view is no longer
        needed, i.e, the user clicks close.

        Params:
         - interaction (discord.Interaction): The button interaction.
        """
        await self.message.delete()