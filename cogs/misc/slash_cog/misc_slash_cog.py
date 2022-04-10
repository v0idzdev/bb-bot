"""
Contains miscellaneous commands to be used for fun.
"""

import datetime
import random
import discord
import humanize

from discord import app_commands
from discord.ext import commands
from utils import TwitchBroadcast, ViewYoutubeButton

from ..misc_utils import fetch_from_youtube


class MiscSlashCog(commands.Cog):
    """
    🎲 Contains miscellaneous commands.
    """

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command()
    @app_commands.describe(name="❓ The Twitch streamer's username.")
    async def twitch(self, interaction: discord.Interaction, *, name: str):
        """
        🎲 Shows information about a Twitch stream.

        ❓ This command is also available as a prefix command.

        Usage:
        ```
        /twitch <streamer name>
        ```
        Or:
        ```
        ~choose <streamer name>
        """
        await interaction.response.defer()

        client = self.client.twitch
        name = name.lower()
        broadcaster_data = await client.connect("helix/users", login=name)
        broad_list = broadcaster_data["data"]

        if broad_list:
            broadcaster_id = broad_list[0]["id"]

            broadcaster_name = broad_list[0]["display_name"]
            json = await client.connect("helix/streams", user_id=str(broadcaster_id))

            if not json["data"]:
                return await interaction.followup.send(
                    f":x: {broadcaster_name} isn't live.",
                    ephemeral=True,
                )

            stream: TwitchBroadcast = await client.return_information(json)
            stream.thumbnail.seek(0)
            file = discord.File(fp=stream.thumbnail, filename="stream.png")

            game_cover = stream.game_image
            game_name = stream.game_name
            view_count = stream.viewer_count
            username = stream.username
            stream_title = stream.stream_title
            started_at = stream.started_at

            on_going_for = humanize.precisedelta(
                datetime.datetime.utcnow() - started_at, format="%0.0f"
            )

            embed = discord.Embed(
                title=stream_title,
                timestamp=datetime.datetime.utcnow(),
                url=stream.stream_url,
            )

            embed.set_image(url="attachment://stream.png")
            embed.set_thumbnail(url=game_cover)
            embed.add_field(name="Stream Time", value=on_going_for)
            embed.add_field(name="Username", value=username)
            embed.add_field(name="Viewer Count", value=view_count)
            embed.add_field(name="Category", value=game_name)

            return await interaction.followup.send(embed=embed, file=file)

        return await interaction.followup.send(
            f":x: I couldn't find a streamer with the name '{name}'.", ephemeral=True
        )

    @app_commands.command()
    @app_commands.describe(choices="❓ Choices separated by spaces.")
    async def choose(self, interaction: discord.Interaction, *, choices: str):
        """
        🎲 Chooses a random option from a list of choices.

        ❓ This command is also available as a prefix command.

        Usage:
        ```
        /choose <...choices>
        ```
        Or:
        ```
        ~choose <question>
        """
        await interaction.response.defer()
        choices = [choice.strip().lower() for choice in choices.split(" ")]

        # Display some error messages if the user's input is invalid.
        # This is because it's kinda awkward to do this in the on_command_error event.
        if len(choices) < 1:
            return await interaction.followup.send(
                f":x: You need to give me choices to choose from.",
                ephemeral=True,
            )

        if len(choices) == 1:
            return await interaction.followup.send(
                f":x: I need more than one choice!",
                ephemeral=True,
            )

        embed = discord.Embed(
            title=f"🎲 I Choose",
            description=f"```{random.choice(choices)}```",
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def meme(self, interaction: discord.Interaction):
        """
        🎲 Sends a random meme from Reddit.

        ❓ This command is also available as a prefix command.

        Usage:
        ```
        /meme
        ```
        Or:
        ```
        ~meme
        """
        await interaction.response.defer()
        response = await self.client.session.get("https://meme-api.herokuapp.com/gimme")
        data = await response.json()
        meme = discord.Embed(title=str(data["title"]))
        meme.set_image(url=str(data["url"]))

        await interaction.followup.send(embed=meme)

    @app_commands.command()
    @app_commands.describe(poll="❓ The question to ask the poll for.")
    async def poll(self, interaction: discord.Interaction, *, poll: str):
        """
        🎲 Creates a simple yes or no poll.

        ❓ This command is also available as a prefix command.

        Usage:
        ```
        /poll <question>
        ```
        Or:
        ```
        ~poll <question>
        ```
        """
        await interaction.response.defer()

        if not poll:
            return await interaction.followup.send(
                f":x: You need to specify a question.",
                ephemeral=True,
            )

        embed = discord.Embed(
            title=f"📢 Poll by **{interaction.user.name}**:",
            description=f"```❓ {poll}```\n",
        )

        embed.set_footer(text="Vote ✔️ Yes or ❌ No.")
        message = await interaction.followup.send(embed=embed)

        await message.add_reaction("✔️")
        return await message.add_reaction("❌")

    @app_commands.command()
    @app_commands.describe(message="❓ The phrase you want the bot to repeat.")
    async def echo(self, interaction: discord.Interaction, *, message: str):
        """
        🎲 Repeats what you say.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~echo <message>
        ```
        Or:
        ```
        /echo <message>
        ```
        """
        await interaction.response.defer()

        if message is None:
            return await interaction.followup.send(
                f":x: You need to tell me what to say.", ephemeral=True
            )

        await interaction.followup.send(message)

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        """
        🎲 Shows your current latency.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~ping
        ```
        Or:
        ```
        /ping
        ```
        """
        await interaction.response.defer()

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"⌛ Your ping is **{round(self.client.latency * 1000)}**ms.",
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.describe(search="❓ The YouTube video to search for.")
    async def youtube(self, interaction: discord.Interaction, *, search: str):
        """
        🎲 Searches for a video on youtube and sends the link.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~youtube <search>
        ```
        Or:
        ```
        /youtube <search>
        ```
        """
        await interaction.response.defer()

        if search is None:
            return await interaction.followup.send(
                f":x: You need to tell me what to search for.", ephemeral=True
            )

        embed, url = await fetch_from_youtube(search)
        await interaction.followup.send(embed=embed)

        # Ask if they would like to view the video in Discord
        embed = discord.Embed(
            title="🎲 View in Discord?",
            description="❓ Click View In Discord to view the video in this text channel.",
        )
        view = ViewYoutubeButton(url, interaction, timeout=60)
        view.message = await interaction.followup.send(embed=embed, view=view)


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(MiscSlashCog(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(MiscSlashCog(client))
