"""
Contains all of the events that the client will listen to.
"""

import discord
import asyncio

from client import Client
from discord.ext import commands


class EventHandler(commands.Cog):
    """
    Responsible for handling all events that the bot will listen to.
    """

    def __init__(self, client: Client) -> None:
        self.client = client
        self.reactionroles_database_filepath = client.database_paths["reactionroles"]

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
        if user.bot:
            return

        message: discord.Message = discord.utils.find(
            lambda cached_message: reaction.message == cached_message,
            self.client.cached_messages,
        )

        for existing_reaction in message.reactions:
            users = {user async for user in existing_reaction.users()}

            if user in users and str(existing_reaction) != str(reaction):
                await message.remove_reaction(existing_reaction.emoji, user)

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
        reaction_roles = self.client.cache.reactionroles

        for reaction_role in reaction_roles:
            if reaction_role["msg_id"] == message.id:
                reaction_roles.remove(reaction_role)

        self.client.update_json(self.reactionroles_database_filepath, reaction_roles)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Executes when the bot has loaded.
        """
        print(f"Loaded\nName: {self.client.user.name} // ID: {self.client.user.id}")

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
