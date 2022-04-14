"""
Module `blacklist_view` contains a base class for blacklist UI views.
Inheriting from it enforces certain methods to be present.
"""
import abc
import apis
import discord
import base
import ui
import motor.motor_asyncio

from typing import Awaitable, Optional, Union


class BlacklistView(base.View):
    """
    Class `BlacklistView` defines an abstract class that inherits from `base.View`, and
    defines abstract `send_modal`, `submit`, and `abort` methods for common button callbacks.
    """
    def __init__(
        self,
        blacklist_dropdown,
        mongo_client: motor.motor_asyncio.AsyncIOMotorClient,
        *,
        title: str,
        placeholder: str,
    ) -> None:
        """
        Creates a blacklist view, composed of a modal that allows users to enter words, and a dropdown
        menu to allow users to choose words to blacklist. This also contains a set of three buttons, for
        entering a new word, aborting, and submitting the list of words.

        Params:
         - blacklist_dropdown (ui.selects.BlacklistDropdown): The dropdown object to use.
         - mongo_client (motor.motor_asyncio.AsyncIOMotorClient): The mongo client the bot uses.

        Returns:
         - A `BlacklistView` instance.
        """
        super().__init__()

        self.title = title
        self.placeholder = placeholder
        self._blacklist_database = apis.mongo.Collection(mongo_client["bb_bot"], "blacklist")
        self._blacklist_dropdown = blacklist_dropdown
        self.add_item(self._blacklist_dropdown)

    @abc.abstractmethod
    async def submit(self, interaction: discord.Interaction, button: discord.Button) -> Awaitable:
        """
        Abstract method for a blacklist submit button callback. This must be decorated
        using the `@discord.ui.button` decorator.

        Params:
         - interaction (discord.Interaction): The discord interaction object.
         - button (discord.Button): The button object that triggers this callback.
        """
        ...

    @discord.ui.button(label="Abort", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def abort(self, interaction: discord.Interaction, button: discord.Button) -> None:
        """
        This method is called when the user clicks the abort button. The method sends an
        ephemeral message and disables all buttons in the view.

        Params:
         - interaction (discord.Interaction): The discord interaction object.
         - button (discord.Button): The button object that triggers this callback.
        """
        await interaction.response.send_message(f"👍🏻 Aborting command.", ephemeral=True)
        await self.disable_all_buttons(interaction)

    @discord.ui.button(label="Enter a New Word", style=discord.ButtonStyle.blurple, emoji="💬")
    async def send_modal(self, interaction: discord.Interaction, button: discord.Button) -> Awaitable:
        """
        This method is called when the enter word button is clicked. This method sends
        the user a modal, where they can enter a word into the list of words.

        Params:
         - interaction (discord.Interaction): Discord interaction object.
         - button (discord.Button): The button that will trigger this callback.
        """
        modal = ui.modals.BlacklistModal(self, self._blacklist_dropdown, self.title, self.placeholder)
        await interaction.response.send_modal(modal)


    async def disable_all_buttons(self, interaction: discord.Interaction=None) -> None:
        """
        This method overrides `base.View` and implements interaction checks differently
        to it. This method prevents users who weren't the original command author from
        interacting with the view.

        Params:
         - interaction (discord.Interaction): The discord interaction object.
        """
        interaction = interaction or self
        self._blacklist_dropdown.disabled = True

        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)
        self.stop()