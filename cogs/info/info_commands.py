import discord
from discord.ext import commands


async def return_awaitable(
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

    embed = discord.Embed(
        title=f"💡 Join Date",
        description=f"👋🏻 **{member.joined_at}**",  # Fix timestamp
    )

    embed.set_author(icon_url=member.avatar.url, name=member.display_name)

    return await return_awaitable(is_interaction, embed, ctx)


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

    return await return_awaitable(is_interaction, embed, ctx)


async def perms_callback(
    ctx: discord.Interaction | commands.Context, member: discord.Member = None
):
    ...
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

    return await return_awaitable(is_interaction, embed, ctx)
