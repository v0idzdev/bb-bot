"""
Module `blacklist_append` contains the class `BlacklistAppendView`, which provides
a UI component for adding words to a blacklist.
"""
import discord
import base


class BlacklistAppendView(base.BlacklistView):
    """
    Class `BlacklistAppendDropdown` provides a user interface view
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
        add_words = set(entered_words) - set(blacklisted_words)

        if not add_words:
            return await interaction.followup.send(
                f"❌ Those words are already in the blacklist.",
                ephemeral=True,
            )

        blacklisted_words.extend(add_words)
        await self._blacklist_database.upsert({"_id": guild_id, "blacklisted_words": blacklisted_words})

        embed = discord.Embed(
            title=f"🛠️ Words Successfully Added",
            description=" ".join(f"`{word}`" for word in add_words),
        )

        if len(entered_words) > len(add_words):
            embed.set_footer(text="⚠️ Some words were duplicates and were not added.")

        await interaction.followup.send(embed=embed)
        await self.disable_all_buttons()