"""
Contains all of the events that the client will listen to.
"""

import nextcord
import start
import json

from nextcord.ext import commands

# This is the filepath for the reaction roles data
FILEPATH = 'files/reactionroles.json'


class EventHandler(commands.Cog):
    """
    Responsible for handling all events that the bot will listen to.
    """
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    async def _add_or_remove_role(
        self, payload: nextcord.RawReactionActionEvent, client: commands.Bot, type: str
    ):
        """
        Adds or removes a role from a user.
        """
        guild: nextcord.Guild = client.get_guild(payload.guild_id)
        roles = guild.roles

        match type:

            case 'add':
                member = payload.member
                action = member.add_roles

            case 'remove':
                member: nextcord.Member = guild.get_member(payload.user_id)
                action = member.remove_roles

        if member.bot:
            return

        with open(FILEPATH) as file:
            data = json.load(file)

        for item in data:
            # Check if the reaction emoji and message are the ones used to give a user
            # a specific role, or if the role has been deleted
            if item['emoji'] != payload.emoji.name or item['msg_id'] != payload.message_id \
            or item['role_id'] not in [role.id for role in guild.roles]:
                continue

            # If not, either add/remove the role
            role = nextcord.utils.get(roles, id=item['role_id'])
            await action(role)

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        """
        Sends a welcome message when a member joins a server.
        """
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"👋🏻 Welcome, **{member.name}**.")

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        """
        Sends a welcome message when a member leaves a server.
        """
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"👋🏻 Goodbye, **{member.name}**.")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        """
        Called when a message is sent.
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
    async def on_reaction_add(self, reaction: nextcord.Reaction, user: nextcord.User):
        """
        Prevents users from voting more than once on a poll.
        """
        user = reaction.message.author
        cached = nextcord.utils.get(self.client.cached_messages, id=reaction.message.id)

        if user.id == self.client.user.id:
            return

        for react in cached.reactions:
            users = await react.users().flatten()

            if any({user not in users, user.bot, str(react) == str(reaction.emoji)}):
                continue

            await cached.remove_reaction(react.emoji, user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        await self._add_or_remove_role(payload, self.client, 'add')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: nextcord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        await self._add_or_remove_role(payload, self.client, 'remove')

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message):
        """
        Deletes reaction role messages that correspond to a deleted role. Removes the
        entry for that reaction role in the JSON file.
        """
        with open(FILEPATH) as file:
            data: list = json.load(file)

        for item in data:
            if item['msg_id'] == message.id:
                await message.delete()
                data.remove(item)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Executes when the bot has loaded.
        """
        print(f'Loaded {self.client.user.name} successfully.')

        task_handler = self.client.cogs.get('TaskHandler')
        tasks = [
            'change_presence',
            'clean_json_file'
        ]

        for task in tasks:
            await task_handler.__getattribute__(task).start()

        # await self.client.cogs.get('TaskHandler').__getattribute__('change_presence').start()
        # await self.client.cogs.get('TaskHandler').__getattribute__('clean_json_file').start()


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(EventHandler(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(EventHandler(client))