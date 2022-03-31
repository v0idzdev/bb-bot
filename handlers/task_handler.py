import threading

import discord
from discord.ext import commands, tasks

# JSON file containing reaction role data
FILEPATH = "files/reactionroles.json"


class TaskHandler(commands.Cog):
    """
    Manages and schedules timed async background tasks.
    """

    def __init__(self, client: commands.Bot):
        self.client = client

    def do_process(self):
        print(f"[INFO] Running clean_json_file.\n")
        data = self.client.cache.reactionroles

        for guild in self.client.guilds:
            for item in list(filter(lambda item: item["guild_id"] == guild.id, data)):
                if item["role_id"] not in [role.id for role in guild.roles]:
                    data.remove(item)

        self.client.update_json(FILEPATH, data)

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
        print(f"[INFO] Running change_presence.\n")
        activity = next(self.client.possible_status)

        await self.client.change_presence(activity=discord.Game(activity))


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(TaskHandler(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(TaskHandler(client))
