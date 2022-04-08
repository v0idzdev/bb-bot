import re
import discord
import datetime

from dulwich.repo import Repo
from dulwich.porcelain import tag_list
from discord.ext import commands
from client import Client


async def send_embed(
    is_interaction: bool,
    embed: discord.Embed,
    ctx: commands.Context | discord.Interaction,
):
    """
    Returns a coroutine that sends the appropriate embed, depending on the command type.
    """
    if is_interaction:
        return await ctx.followup.send(embed=embed, ephemeral=True)

    return await ctx.send(embed=embed)


async def joined_callback(
    ctx: discord.Interaction | commands.Context, member: discord.Member = None
):
    is_interaction = isinstance(ctx, discord.Interaction)

    if is_interaction:
        await ctx.response.defer()

    if member is None:  # if no user is provided, show info about the member
        member = ctx.user if is_interaction else ctx.author

    date = member.joined_at.strftime("%d/%m/%Y")
    time = member.joined_at.strftime("%I:%M %p")

    embed = discord.Embed(
        title=f"💡 Join Date",
        description=f"👋🏻 **{date}** | *{time}*",
    )

    embed.set_author(icon_url=member.avatar.url, name=member.display_name)

    return await send_embed(is_interaction, embed, ctx)


async def toprole_callback(
    ctx: discord.Interaction | commands.Context, member: discord.Member = None
):
    is_interaction = isinstance(ctx, discord.Interaction)

    if is_interaction:
        await ctx.response.defer()

    if member is None:  # if no user is provided, show info about the member
        member = ctx.user if is_interaction else ctx.author

    embed = discord.Embed(
        title=f"💡 Top Role",
        description=f"🌟 **{member.top_role.name}**",
    )

    embed.set_author(icon_url=member.avatar.url, name=member.display_name)

    return await send_embed(is_interaction, embed, ctx)


async def perms_callback(
    ctx: discord.Interaction | commands.Context, member: discord.Member = None
):
    is_interaction = isinstance(ctx, discord.Interaction)

    if is_interaction:
        await ctx.response.defer()

    if member is None:  # if no user is provided, show info about the member
        member = ctx.user if is_interaction else ctx.author

    perms = "\u200b".join(
        f"`{perm}` " for perm, value in member.guild_permissions if value
    )

    embed = discord.Embed(
        title=f"💡 Permissions",
        description=perms,
    )

    embed.set_author(icon_url=member.avatar.url, name=member.display_name)

    return await send_embed(is_interaction, embed, ctx)


async def botinfo_callback(ctx: discord.Interaction | commands.Context, client: Client):
    is_interaction = isinstance(ctx, discord.Interaction)

    if is_interaction:
        await ctx.response.defer()

    embed = discord.Embed(
        title="💡 Bot Information",
        description="❓ Some information about BB.Bot.",
        timestamp=datetime.datetime.utcnow()
    )

    # Find the current stable + dev release names
    repo = Repo(".")
    tags = [str(tag)[3: -1] for tag in tag_list(repo)] # Remove b'v and ' from b'v1.1.5' etc

    # ! bad code, just a test
    is_stable_version_regex = re.compile(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)") # x.x.x
    is_stable_version = lambda tag: is_stable_version_regex.match(tag) is not None and len(tag) == 5 # bad

    stable_version = list(filter(is_stable_version, tags))[-1]
    development_version = tags[-1]

    embed.set_footer(text=f'➕ BB.Bot is running on {len(client.guilds)} servers.')
    embed.add_field(name='🎁 Versions', value=f'Stable: **{stable_version}** | Development: **{development_version}**', inline=False)
    embed.add_field(name='🌍 Language', value='Python **3.10.2**', inline=False)
    embed.set_author(
        name="Matthew Flegg",
        url="https://github.com/matthewflegg",
        icon_url="https://imagemagick.org/image/convex-hull.png",
    )

    return await send_embed(is_interaction, embed, ctx)
