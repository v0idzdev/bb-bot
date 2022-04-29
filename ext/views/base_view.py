"""
Module `base_view` contains the `BaseView` class, which
provides common functionality.
""" 
import discord

from ext import utils
from typing import Any

from discord import (
    ui,
    app_commands
)


class BaseView(ui.View):
    """
    Class `BaseView` is a subclass of `discord.ui.View` that
    implements `interaction_check` and `disable_all_buttons`.
    """
    def __init__(self, interaction: discord.Interaction, **kwargs: Any) -> None:
        """
        Creates an instance of `discord.ui.View` that implements
        an `interaction_check` and a `disable_all_buttons` method.

        Params:
         - interaction (discord.Interaction): The interaction the command was invoked with.
         - message (discord.Message): Pass the message the view is sent in.
         - **kwargs (Any): Any keyword arguments that `discord.ui.View` accepts.
        """
        super().__init__()
        self.command_author_id = interaction.user.id
        self.message: discord.Message = None
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Prevents users who weren't the command sender from interacting
        with the view component.

        Params:
         - interaction (discord.Interaction): The interaction used with the view.
        
        Returns:
         - A `bool`. If false, the view will not execute any callbacks.
        """
        if interaction.user.id == self.command_author_id:
            return True
        
        error_embed = utils.create_error_embed("This isn't your interaction.")
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        return False

    async def disable_all_buttons(self) -> None:
        """
        Disables all buttons that are attached to the view component. This
        is usually done when a view should be closed, to prevent errors.

        Params:
         - interaction (discord.Interaction): The interaction used with the view.
        """
        for child in self.children:
            child.disabled = True

        await self.message.edit(view=self)
        self.stop()