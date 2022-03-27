from typing import Optional

import discord
from discord.ext import commands

FILEPATH = "files/blacklist.json"

class ClearMessagesView(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def on_timeout(self) -> None:
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
        await interaction.response.defer() # manually defer interaction for an increased respond time

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
        await interaction.response.send_message('👍🏻 Aborting command!')
        await self.disable_all_buttons(interaction)

class BlacklistClearButton(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, data: dict, timeout: Optional[float] = 180):
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
        await interaction.response.defer() # manually defer interaction for an increased respond time

        server_id = str(interaction.guild.id)
        server = self.blacklist.get(server_id)

        if server:
            del self.blacklist[server_id]

            interaction.client.update_json('./files/blacklist.json', self.blacklist)
            embed = discord.Embed(title='🛠️ Blacklist successfully deleted.')

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
