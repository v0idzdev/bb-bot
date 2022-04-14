"""
Module `blacklist_remove_view` contains class `BlacklistRemoveView`, which
provides a user interface for adding words to the blacklist for a server.
"""
import discord
import base


class BlacklistRemoveView(base.BlacklistView):
    """
    Class `BlacklistRemoveView` provides a user interface view
    for adding words to a blacklist.
    """
    @discord.ui.button(label="Submit Words", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def submit(self, interaction: discord.Interaction, button: discord.Button) -> None:
        """
        This method is called when the submit words button is clicked. This method adds
        all words that are in the list of words the user added to the blacklist database.
        """
        await interaction.response.defer()
        entered_words = [value.strip().lower() for value in self._blacklist_dropdown.words]

        if not entered_words:
            return await interaction.followup.send(
                f"❌ You need to have at least one word selected!",
                ephemeral=True,
            )

        guild_id = interaction.guild.id
        blacklisted_words: list = await self._blacklist_database.find(guild_id)

        if blacklisted_words is None:
            return await interaction.followup.send(
                f"❌ This server does not have any words blacklisted.",
                ephemeral=True,
            )

        remove_words = set(entered_words) & set(blacklisted_words)

        if not remove_words:
            return await interaction.followup.send(
                f"❌ Those words are already in the blacklist.",
                ephemeral=True,
            )

        blacklisted_words.remove(remove_words)
        await self._blacklist_database.remove({"_id": guild_id, "blacklisted_words": blacklisted_words})

        embed = discord.Embed(
            title=f"🛠️ Words Successfully Removed",
            description=" ".join(f"`{word}`" for word in remove_words),
        )

        if len(entered_words) > len(remove_words):
            embed.set_footer(text="⚠️ Some words were duplicates and were not removed.")

        await interaction.followup.send(embed=embed)
        await self.disable_all_buttons()