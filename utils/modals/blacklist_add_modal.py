import discord


class BlacklistAddModal(discord.ui.Modal):
    """
    Describes a modal that users can enter words to add to the blacklist into.
    """

    def __init__(
        self,
        view: discord.ui.View,
        drop: discord.ui.Select,
        *,
        title: str = "🔒 Add a Word to the Blacklist",
    ):
        super().__init__(title=title)

        self.view = view
        self.drop = drop

        self.text = discord.ui.TextInput( # Takes the user's input
            label="Word", placeholder="🔑 Enter a word to blacklist:", max_length=100
        )

        self.add_item(self.text)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Called when the user submits the modal.
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