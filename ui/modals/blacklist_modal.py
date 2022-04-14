"""
Module `blacklist_modal` contains class `BlacklistModal`, which is a base
class for blacklist word entry forms.
"""
import base
import discord


class BlacklistModal(discord.ui.Modal):
    """
    Class `BlacklistModal` provides an input form for entering a
    word to add to a server's blacklist.
    """
    def __init__(
        self,
        view: base.BlacklistView,
        drop,
        *,
        title: str,
        placeholder: str
    ) -> None:
        """
        Creates an instance of `BlacklistModal`, which can be used to add
        or remove words from the server's blacklist.

        Params:
         - view (cogs.admin.abc.BlacklistView): The view that this modal is a component of.
         - drop (cogs.admin.abc.BlacklistDropdown): The dropdown menu this modal will use.
         - title (str): The title/header text for the modal.
         - placeholder (str): The placeholder input for the text input field.
        """
        super().__init__(title=title)

        self.view = view
        self.drop = drop

        self.text = discord.ui.TextInput(label="Word", placeholder=placeholder)
        self.add_item(self.text)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        This method is called when the data in the modal is submitted.

        Params:
         - interaction (discord.Interaction): The interaction object.
        """
        await interaction.response.defer()

        if not self.text.value:
            return

        if self.drop.options[0].label == "\u200b":
            self.drop.options.pop(0)

        option = discord.SelectOption(label=self.text.value, default=True)

        self.drop.append_option(option)
        self.drop.max_values = len(self.drop.options)
        self.drop.words.append(self.text.value)

        await interaction.message.edit(view=self.view)
        return await super().on_submit(interaction=interaction)