"""
Contains all of the events that the client will listen to.
"""

import discord
from discord.ext import commands

# This is the filepath for the reaction roles data
FILEPATH = "files/reactionroles.json"


class EventHandler(commands.Cog):
    """
    Responsible for handling all events that the bot will listen to.
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    async def _add_or_remove_role(
        self, payload: discord.RawReactionActionEvent, client: commands.Bot, type: str
    ):
        """
        Adds or removes a role from a user.
        """
        guild: discord.Guild = client.get_guild(payload.guild_id)

        if type == "add":
            member = payload.member
            action = member.add_roles

        if type == "remove":
            member: discord.Member = guild.get_member(payload.user_id)
            action = member.remove_roles

        if member.bot:
            return

        data = self.client.cache.reactionroles
        roles = guild.roles

        for item in data:
            # Check if the reaction emoji and message are the ones used to give a user
            # a specific role, or if the role has been deleted
            if (
                item["emoji"] != payload.emoji.name
                or item["msg_id"] != payload.message_id
                or item["role_id"] not in [role.id for role in guild.roles]
            ):
                continue
            # If not, either add/remove the role
            role = discord.utils.get(roles, id=item["role_id"])
            await action(role)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Sends a welcome message when a member joins a server.
        """
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"👋🏻 Welcome, **{member.name}**.")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Sends a welcome message when a member leaves a server.
        """
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"👋🏻 Goodbye, **{member.name}**.")

    @commands.Cog.listener()  # This throws an AttributeError but it isn't really an issue
    async def on_message(self, message: discord.Message):
        """
        Called when a message is sent.
        """
        if not message.guild or message.author.bot:
            return

        blacklist = self.client.cache.blacklist

        if (
            self.client.command_prefix(self.client, message) in message.content
            or (id := str(message.guild.id)) not in blacklist
        ):
            return
        for wordlist in (
            words_msg := set(
                msg.lower() for msg in message.content.split(" ")
            ),  # Words in the message
            words_ban := set(blacklist.get(id)),  # Words blacklisted in the server
        ):
            wordlist = {word.strip().lower() for word in wordlist}

        if words_msg & words_ban:  # If any banned words are in the message
            await message.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Prevents users from voting more than once on a poll.
        """
        cached = discord.utils.get(self.client.cached_messages, id=reaction.message.id)

        if user.id == self.client.user.id:
            return

        for react in cached.reactions:
            users = [user async for user in react.users()]

            if any({user not in users, user.bot, str(react) == str(reaction.emoji)}):
                continue

            await cached.remove_reaction(react.emoji, user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        await self._add_or_remove_role(payload, self.client, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        await self._add_or_remove_role(payload, self.client, "remove")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        Deletes reaction role messages that correspond to a deleted role. Removes the
        entry for that reaction role in the JSON file.
        """
        data = self.client.cache.reactionroles

        for item in data:
            if item["msg_id"] == message.id:
                await message.delete()
                data.remove(item)

        self.client.update_json(FILEPATH, data)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Executes when the bot has loaded.
        """
        print(
            f"LOADED {self.client.user.name} SUCCESSFULLY.\n\n---------- LOGS: ----------\n"
        )

        task_handler = self.client.cogs.get("TaskHandler")
        tasks = ["change_presence", "clean_json_file"]

        for task in tasks:
            task_handler.__getattribute__(task).start()


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(EventHandler(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(EventHandler(client))
