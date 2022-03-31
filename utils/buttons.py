import black
import discord

from typing import Optional
from discord.ext import commands

FILEPATH = "files/blacklist.json"


class ClearMessagesView(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def on_timeout(self) -> None:
        """
        Called when the view times out.
        """
        await self.disable_all_buttons()

    async def disable_all_buttons(self, interaction: discord.Interaction = None):
        """
        Disables all buttons.
        """
        interaction = interaction or self

        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Prevents users who weren't the command sender from using buttons.
        """
        if interaction.user.id == self.ctx.author.id:
            return True
        else:
            await interaction.response.send_message(":x: This isn't your interaction!")
            return False

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def yes(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the yes button.
        """
        await interaction.response.defer()  # manually defer interaction for an increased respond time

        channel_pos = interaction.channel.position
        category = interaction.channel.category
        new_channel = await interaction.channel.clone()

        await new_channel.edit(category=category, position=channel_pos)
        await interaction.channel.delete()

        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def no(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the no button.
        """
        await interaction.response.send_message("👍🏻 Aborting command!")
        await self.disable_all_buttons(interaction)


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
            await interaction.response.send_message(":x: This isn't your interaction!")
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
            embed = discord.Embed(title="🛠️ Blacklist successfully deleted.")

            await interaction.followup.send(embed=embed)
            await self.disable_all_buttons(interaction)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def no(self, interaction: discord.Interaction, _: discord.Button):
        """
        Callback method for the no button.
        """
        mention = interaction.user.mention

        await interaction.response.send_message(f":thumbsup: {mention}: Ok!")
        await self.disable_all_buttons(interaction)


class BlacklistModal(discord.ui.Modal):
    def __init__(
        self,
        view: discord.ui.View,
        drop: discord.ui.Select,
        *,
        title: str = "🔑 Enter a word to blacklist:",
    ) -> None:
        super().__init__(title=title)
        self.view = view
        self.drop = drop
        self.text = discord.ui.TextInput(
            label="Word", placeholder="🔑 Enter a word to blacklist:", max_length=100
        )
        self.add_item(self.text)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if self.text.value:
            if self.drop.options[0].label == "\u200b":
                self.drop.options.pop(0)
            opt = discord.SelectOption(label=self.text.value, default=True)
            self.drop.append_option(opt)
            self.drop.max_values = len(self.drop.options)
            self.drop.words.append(self.text.value)
            await interaction.message.edit(view=self.view)
            return await super().on_submit(interaction=interaction)


class BlacklistDropdown(discord.ui.Select):
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        options = [discord.SelectOption(label="\u200b", default=False)]
        self.words = []
        super().__init__(
            placeholder="📃 Choose words to blacklist...",
            min_values=1,
            max_values=len(options),
            options=options,
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
                f"❌ {interaction.user.mention}: You need to select one or more than one words to blacklist!",
                ephemeral=True,
            )
        self.words = self.values
        return


class DropdownView(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, timeout: Optional[float] = 180):
        super().__init__()
        self.ctx = ctx
        self.drop = BlacklistDropdown(ctx)
        self.add_item(self.drop)

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

    async def disable_all_buttons(self, interaction: discord.Interaction = None):
        """
        Disables all buttons.
        """
        interaction = interaction or self
        self.drop.disabled = True
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(
        label="Enter a New Word", style=discord.ButtonStyle.blurple, emoji="💬"
    )
    async def send_modal(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        modal = BlacklistModal(self, self.drop)
        await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="Submit Words", style=discord.ButtonStyle.green, emoji="👍🏻"
    )
    async def submit(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        values = self.drop.words
        id = str(interaction.guild_id)
        if not values:
            print(values)
            return await interaction.followup.send(
                f"❌ {interaction.user.mention}: You need to have at least one word selected!",
                ephemeral=True,
            )
        blacklist = interaction.client.cache.blacklist
        if id not in blacklist.keys():
            blacklist[id] = []
        words = set(values) - set(blacklist[id])
        if not words:
            return await interaction.followup.send(
                f"❌ {interaction.user.mention}: Sorry. Those words are already in the blacklist.",
                ephemeral=True,
            )
        blacklist[id].extend(words)
        interaction.client.update_json(FILEPATH, blacklist)
        embed = discord.Embed(
            title=f"🛠️ Words successfully added.",
            description=" ".join(f"`{word}`" for word in words),
        )
        if len(values) > len(words):
            embed.set_footer(text="⚠️ Some words were duplicates and were not added.")
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Abort", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def abort(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(
            f"❌ {interaction.user.mention}: Aborting command!", ephemeral=True
        )
        await self.disable_all_buttons(interaction)


class BlacklistRemoveModal(discord.ui.Modal):
    def __init__(
        self,
        view: discord.ui.View,
        drop: discord.ui.Select,
        *,
        title: str="🔑 Enter a word to remove from the blacklist:"
    ) -> None:
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


class BlacklistRemoveView(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, timeout: Optional[float] = 180):
        super().__init__()
        self.ctx = ctx
        self.drop = BlacklistRemoveDropdown(ctx)
        self.add_item(self.drop)

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

    async def disable_all_buttons(self, interaction: discord.Interaction = None):
        """
        Disables all buttons.
        """
        interaction = interaction or self
        self.drop.disabled = True
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(
        label="Enter a New Word", style=discord.ButtonStyle.blurple, emoji="💬"
    )
    async def send_modal(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        modal = BlacklistRemoveModal(self, self.drop)
        await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="Submit Words", style=discord.ButtonStyle.green, emoji="👍🏻"
    )
    async def submit(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()

        values = self.drop.words
        id = str(interaction.guild.id)

        if not values:
            print(values)

            return await interaction.followup.send(
                f"❌ {interaction.user.mention}: You need to have at least one word selected!",
                ephemeral=True,
            )

        blacklist = interaction.client.cache.blacklist

        if id not in blacklist.keys():
            return await interaction.followup.send(
                f"❌ {interaction.user.mention}: This server does not have any words blacklisted.",
                ephemeral=True
            )

        print(values)
        words = set(values) & set(blacklist[id])
        print(values, words)

        if not words:
            return await interaction.followup.send(
                f"❌ {interaction.user.mention}: Sorry. Those words are not in the blacklist.",
                ephemeral=True,
            )

        for word in words:
            blacklist[id].remove(word)

        interaction.client.update_json(FILEPATH, blacklist)

        embed = discord.Embed(
            title=f"🛠️ Words successfully removed.",
            description=" ".join(f"`{word}`" for word in words),
        )

        if len(values) > len(words):
            embed.set_footer(text="⚠️ Some words were duplicates and were not added.")

        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Abort", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def abort(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(
            f"❌ {interaction.user.mention}: Aborting command!", ephemeral=True
        )
        await self.disable_all_buttons(interaction)