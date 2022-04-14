"""
Module `.blacklist_dropdown` contains class BlacklistDropdown, which is used
for blacklist-related dropdown menus.
"""
import discord

from typing import Union


class BlacklistDropdown(discord.ui.Select):
    """
    Class `BlacklistDropdown` is a base class for blacklist dropdowns.
    It implements an `interaction_check` method and has an abstract
    `callback` method.
    """
    def __init__(
        self,
        command_author: Union[discord.Member, discord.User],
        placeholder: str,
    ) -> None:
        """
        Creates an instance of `BlacklistDropdown`, which is used to provide a
        modal and dropdown menu for entering words to blacklist.

        Params:
         - command_author (Union[discord.Member, discord.User]): The original command user.

        Returns:
         - An instance of `BlacklistDropdown`.
        """
        options = [discord.SelectOption(label="\u200b", default=False)]

        self.words = []
        self._command_author = command_author

        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        This method is called when the submit button is called on the view that this
        dropdown menu is attached to. This method checks for missing words.

        Params:
         - interaction (discord.Interaction): Discord interaction object.
        """
        await interaction.response.defer()

        if not self.values:
            return await interaction.followup.send(
                f"❌ You need to select one or more than one words to blacklist!",
                ephemeral=True,
            )

        self.words = self.values

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        This method prevents users who weren't the original command user from
        interacting with the dropdown.

        Params:
         - interaction (discord.Interaction): Slash command invocation context.
        """
        if interaction.user.id == self._command_author.id:
            return True

        await interaction.response.send_message("❌ You can't use this dropdown!", ephemeral=True)
        return False