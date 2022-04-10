import threading
import discord

from client import Client
from discord.ext import commands, tasks


class TaskHandler(commands.Cog):
    """
    Manages and schedules timed async background tasks.
    """

    def __init__(self, client: Client):
        self.client = client
        self.reactionroles_database_filepath = client.database_paths["reactionroles"]

    def do_process(self):
        data = self.client.cache.reactionroles

        for guild in self.client.guilds:
            for item in list(filter(lambda item: item["guild_id"] == guild.id, data)):
                if item["role_id"] not in [role.id for role in guild.roles]:
                    data.remove(item)

        self.client.update_json(self.reactionroles_database_filepath, data)

    @tasks.loop(seconds=60)
    async def clean_json_file(self):
        """
        Automatically removes deleted roles from the JSON file containing reaction roles.
        """
        cleanup_thread = threading.Thread(
            target=self.do_process, name="Renove Unwanted", daemon=True
        )

        cleanup_thread.start()

    @tasks.loop(seconds=30)
    async def change_presence(self):
        """
        Changes the bot's presence every 30 seconds.
        """
        activity = next(self.client.possible_status)
        await self.client.change_presence(activity=discord.Game(activity))


async def setup(client: Client):
    """
    Registers the cog with the client.
    """
    await client.add_cog(TaskHandler(client))


async def teardown(client: Client):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(TaskHandler(client))
