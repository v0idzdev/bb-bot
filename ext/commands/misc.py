"""
Module `misc` contains the `misc` cog/group, which implements
information commands for BB.Bot.
"""
import datetime
import random
import discord
import humanize
import twitchio
import core

from ext import utils
from discord import app_commands
from discord.ext import commands


class Misc(commands.Cog, name="Miscellaneous"):
    """
    🎲 Contains miscellaneous commands.
    """
    def __init__(self, client: core.DiscordClient):
        self.client = client
        super().__init__()

    @app_commands.command()
    @app_commands.describe(broadcaster="❓ The Twitch streamer's username.")
    async def twitch(self, interaction: discord.Interaction, *, broadcaster: str) -> None:
        """
        🎲 Shows information about a Twitch stream.
        """
        streams = await self.client.twitch_client.fetch_streams(user_logins=[broadcaster])

        if not streams:
            error_embed = utils.create_error_embed(f"The streamer **`{broadcaster}`** is not currently live.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        stream: twitchio.Stream = streams[0]
        current_time = datetime.datetime.utcnow()

        stream_time = humanize.precisedelta(
            current_time-stream.started_at.replace(tzinfo=None),
            format="%0.0f"
        )

        streamer = stream.user.name
        stream_embed = discord.Embed(
            title="🎲 Twitch Stream",
            description=f"**[{stream.title}](https://www.twitch.tv/{streamer})**",
            timestamp=current_time,
            color=self.client.theme,
        ) \
            .set_image(url=stream.thumbnail_url.format(width=1890, height=1050)) \
            .add_field(name="⏳ Stream Time", value=stream_time, inline=False) \
            .add_field(name="🖥️ Streamer Name", value=stream.user.name, inline=False) \
            .add_field(name="🚀 Viewer Count", value=stream.viewer_count, inline=False) \
            .add_field(name="❓ Category", value=stream.game_name, inline=False)

        await interaction.response.send_message(embed=stream_embed)

    @app_commands.command()
    @app_commands.describe(choices="❓ The choices to choose from, separated by commas.")
    async def choose(self, interaction: discord.Interaction, *, choices: str):
        """
        🎲 Chooses a random option from a list of choices.
        """
        choices = [x.strip() for x in choices.split(",")]

        if len(choices) <= 1:
            error_embed = utils.create_error_embed("You need to give me at least 2 choices.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        numbered_choices = [f"**`{i + 1}`** — {x}" for i, x in enumerate(choices)]
        
        choice_embed = discord.Embed(
            title="🎲 My Choice",
            description=f"**`{random.choice(choices)}`**",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .add_field(name="❗ Options Given", value="\n".join(numbered_choices))

        await interaction.response.send_message(embed=choice_embed)
    
    @app_commands.command()
    async def meme(self, interaction: discord.Interaction):
        """
        🎲 Sends a random meme from Reddit.
        """
        response = await self.client.session.get("https://meme-api.herokuapp.com/gimme")
        data = await response.json()
        url = data['url']

        meme_embed = discord.Embed(
            title="🎲 Found a Meme",
            description=f"**[{data['title']}]({url})**",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_image(url=f"{url}") \
            .set_footer(text="❓ Try again? Use /meme.")

        await interaction.response.send_message(embed=meme_embed)
    
    @app_commands.command()
    @app_commands.describe(question="❓ The yes/no question to ask for the poll.")
    async def poll(self, interaction: discord.Interaction, *, question: str):
        """
        🎲 Creates a simple yes or no poll for users to vote on.
        """
        if message is None:
            error_embed = utils.create_error_embed("You need to ask a question.")
            return await interaction.response.send_message(embed=error_embed)

        poll_embed = discord.Embed(
            title="🎲 Poll",
            description=f"**`{question}`**",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \
            .set_footer(text="Vote ✔️ Yes or ❌ No.")

        message = await interaction.channel.send(embed=poll_embed)
        await message.add_reaction("✔️")
        await message.add_reaction("❌")
    
    @app_commands.command()
    @app_commands.describe(message="❓ The phrase you want the bot to repeat.")
    async def echo(self, interaction: discord.Interaction, *, message: str):
        """
        🎲 Repeats what you say.
        """
        if message is None:
            error_embed = utils.create_error_embed("You need to tell me what to say.")
            return await interaction.response.send_message(embed=error_embed)
        
        echo_embed = discord.Embed(
            title=f"🎲 Message",
            description=f"**`{message}`**",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \

        await interaction.response.send_message(embed=echo_embed)



async def setup(client: core.DiscordClient) -> None:
    """
    Registers the command group/cog with the discord client.
    All extensions must have a setup function.

    Params:
     - client: (DiscordClient): The client to register the cog with.
    """
    await client.add_cog(Misc(client))


async def teardown(client: core.DiscordClient) -> None:
    """
    De-registers the command group/cog with the discord client.
    This is not usually needed, but is useful to have.

    Params:
     - client: (DiscordClient): The client to de-register the cog with.
    """
    await client.remove_cog(Misc(client))