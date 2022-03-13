"""
Contains all of the events that the client will listen to.
"""

import discord.ext.commands as commands
import modules.utilities.helpers as helpers
import discord
import start
import json


# |-------- EVENT HANDLER --------|


class EventHandler(commands.Cog):
    """
    Responsible for handling all events that the bot will listen to.
    """
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Sends a welcome message when a member joins a server.

        Parameters
        ----------

        member (Member):
            The member that joined the server.
        """
        await helpers.send_message(member, "Welcome")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Sends a welcome message when a member leaves a server.

        Parameters
        ----------

        member (Member):
            The member that left the server.
        """
        await helpers.send_message(member, "Goodbye")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Called when a message is sent.

        Parameters
        ----------

        message (Message):
            The message that was sent.
        """
        with open('files/blacklist.json', 'r') as file:
            blacklist = json.load(file)

        if start.prefix in message.content \
        or (id := str(message.guild.id)) not in blacklist:
            return

        for wordlist in (
            words_msg := set(message.content.split(" ")), # Words in the message
            words_ban := set(blacklist.get(id)) # Words blacklisted in the server
        ):
            wordlist = {word.strip().lower() for word in wordlist}

        if words_msg & words_ban: # If any banned words are in the message
            await message.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Prevents users from voting more than once on a poll.

        Parameters
        ----------

        client (Bot):
            The bot to register the event listener with.

        reaction (Reaction):
            The reaction the user reacted to the poll with.

        user (User):
            The user that reacted to the poll.
        """
        user = reaction.message.author
        cached = discord.utils.get(self.client.cached_messages, id=reaction.message.id)

        if user.id == self.client.user.id:
            return

        for react in cached.reactions:
            users = await react.users().flatten()

            if any({user not in users, user.bot, str(react) == str(reaction.emoji)}):
                continue

            await cached.remove_reaction(react.emoji, user)


# |----- REGISTERING MODULE -----|


def setup(client: commands.Bot):
    """
    Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    client.add_cog(EventHandler(client))