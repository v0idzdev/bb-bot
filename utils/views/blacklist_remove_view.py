import discord

from discord.ext import commands
from typing import Optional
from utils import BlacklistRemoveDropdown, BlacklistRemoveModal

FILEPATH = "files/blacklist.json"


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
                f"❌ This isn't your interaction!",
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

        values = [value.lower() for value in self.drop.words]
        id = str(interaction.guild.id)

        if not values:
            print(values)

            return await interaction.followup.send(
                f"❌ You need to have at least one word selected!",
                ephemeral=True,
            )

        blacklist = interaction.client.cache.blacklist

        if id not in blacklist.keys():
            return await interaction.followup.send(
                f"❌ This server does not have any words blacklisted.",
                ephemeral=True,
            )

        print(values)
        words = set(values) & set(blacklist[id])
        print(values, words)

        if not words:
            return await interaction.followup.send(
                f"❌ Those words are not in the blacklist.",
                ephemeral=True,
            )

        for word in words:
            blacklist[id].remove(word)

        interaction.client.update_json(FILEPATH, blacklist)

        embed = discord.Embed(
            title=f"🛠️ Words Successfully Removed",
            description=" ".join(f"`{word}`" for word in words),
        )

        if len(values) > len(words):
            embed.set_footer(text="⚠️ Some words were duplicates and were not added.")

        await interaction.followup.send(embed=embed)
        await self.disable_all_buttons()

    @discord.ui.button(label="Abort", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def abort(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"👍🏻 Aborting command.", ephemeral=True)
        await self.disable_all_buttons(interaction)
