import datetime
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
        stream: twitchio.Stream = streams[0] or None

        if not stream:
            error_embed = utils.create_error_embed(f"The streamer **`{broadcaster}`** is not currently live.")
            return await interaction.response.send_message(embed=error_embed)

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