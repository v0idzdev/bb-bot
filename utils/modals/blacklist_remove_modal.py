import discord


class BlacklistRemoveModal(discord.ui.Modal):
    def __init__(
        self,
        view: discord.ui.View,
        drop: discord.ui.Select,
        *,
        title: str="🔒 Remove a Word From the Blacklist"
    ):
        super().__init__(title=title)

        self.view = view
        self.drop = drop
        self.text = discord.ui.TextInput(
            label="Word", placeholder="🔑 Enter a word to remove from the blacklist:", max_length=100
        )

        self.add_item(self.text)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        text_value = self.text.value

        if not text_value:
            return

        if self.drop.options[0].label == "\u200b":
            self.drop.options.pop(0)

        option = discord.SelectOption(label=text_value, default=True)

        self.drop.append_option(option)
        self.drop.max_values = len(self.drop.options)
        self.drop.words.append(text_value)

        await interaction.message.edit(view=self.view)
        return await super().on_submit(interaction=interaction)