"""
Module `clear_messages_view` contains class `ClearMessages`, which is a UI component
that prompts the user to continue/abort when asked to delete all messages in a
text channel. Used in `bot.cogs.admin_cog`. Created using the `/admin clear` command.
"""
import base
import discord


class ClearMessagesView(base.View):
    """
    Class `ClearMessages` provides yes/no buttons when the user
    is prompted to clear all messages from a channel.
    """
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍🏻")
    async def yes(self, interaction: discord.Interaction, _: discord.Button):
        """
        This method is called when the user clicks yes when prompted to delete
        all messages in a channel, and then deletes the messages.

        Params:
         - interaction (discord.Interaction): Slash command invocation context.
         - _: (discord.Button): The button object that this callback will be for.
        """
        await interaction.response.defer()

        channel_pos = interaction.channel.position
        category = interaction.channel.category
        new_channel = await interaction.channel.clone()

        await new_channel.edit(category=category, position=channel_pos)
        await interaction.channel.delete()

        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎🏻")
    async def no(self, interaction: discord.Interaction, _: discord.Button):
        """
        This method is called when the user clicks no when prompted to delete
        all messages in a channel, and then deletes the messages.

        Params:
         - interaction (discord.Interaction): Slash command invocation context.
         - _: (discord.Button): The button object that this callback will be for.
        """
        await interaction.response.send_message("👍🏻 Aborting command.", ephemeral=True)
        await self.disable_all_buttons(interaction)