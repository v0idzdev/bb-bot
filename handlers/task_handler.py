import nextcord
import start
import json

from nextcord.ext import commands, tasks

# JSON file containing reaction role data
FILEPATH = 'files/reactionroles.json'


class TaskHandler(commands.Cog):
    """
    Manages and schedules timed async background tasks.
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @tasks.loop(seconds=60)
    async def clean_json_file(self):
        """
        Automatically removes deleted roles from the JSON file containing reaction roles.
        """
        print(f'[TASK] Running <<clean_json_file>>.')

        with open(FILEPATH) as file:
            data: list = json.load(file)

        for guild in self.client.guilds:
            for item in list(filter(lambda item: item['guild_id'] == guild.id, data)):
                if item['role_id'] not in [role.id for role in guild.roles]:
                    data.remove(item)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)

    @tasks.loop(seconds=30)
    async def change_presence(self):
        """
        Changes the bot's presence every 30 seconds.
        """
        print(f'[TASK] Running <<change_presence>>.')

        activity = next(start.status)
        await self.client.change_presence(activity=nextcord.Game(activity))


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(TaskHandler(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(TaskHandler(client))