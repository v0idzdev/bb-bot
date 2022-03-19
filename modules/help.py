"""
Contains the help command.
"""

import nextcord.ext.commands as commands
import nextcord
import start


# |---------- COMMANDS ----------|


@commands.command()
async def help(ctx: commands.Context):
    """
    Generates an embed that links to the documentation page.

    Parameters
    ----------

    ctx: (Context)
        Command invocation context.
    """
    embed = nextcord.Embed(
        title="Beep Boop Bot Documentation",
        color=start.colour,
        url="https://github.com/matthewflegg/beepboop/blob/main/README.md",
        description="View the official commands list for Beep Boop Bot on GitHub.",
    )

    embed.set_author(
        name="Matthew Flegg",
        url="https://github.com/matthewflegg",
        icon_url="https://imagemagick.org/image/convex-hull.png",
    )

    embed.set_thumbnail(
        url="https://media.istockphoto.com/vectors/robot-avatar-icon-vector-id908807494?k=20&m=908807494&s=612x612&w=0&h=N050SIC8pgzsf_LaJT-ZyEE6HHMXLU5PYfMpixuinas="
    )

    embed.set_footer(
        text="Contribute to the open source Beep Boop Bot GitHub repository."
    )

    await ctx.send(embed=embed)


# |---- REGISTERING COMMANDS ----|


def setup(client: commands.Bot):
    """
    Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    client.add_command(help)
