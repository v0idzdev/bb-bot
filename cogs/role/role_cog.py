"""
Contains a cog that handles reaction roles/self roles.
"""

import discord
import json

from client import Client
from discord.ext import commands


class RoleCog(commands.Cog, name="Roles"):
    """
    🏷️ Contains role commands.
    """

    def __init__(self, client: Client):
        self.client = client
        self.reactionroles_database_filepath = client.database_paths["reactionroles"]

    @commands.command(aliases=["crr"])
    @commands.has_permissions(manage_roles=True)
    async def reactrole(
        self, ctx: commands.Context, emoji, role: discord.Role, *, message: str
    ):
        """
        🏷️ Creates a reaction role message.

        Usage:
        ```
        ~reactrole | ~crr <emoji> <@role> <message>
        ```
        """
        embed = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embed)

        await msg.add_reaction(emoji)

        database = self.client.cache.reactionroles
        database.append(
            {
                "guild_id": ctx.guild.id,
                "name": role.name,
                "role_id": role.id,
                "emoji": emoji,
                "msg_id": msg.id,
            }
        )

        self.client.update_json(self.reactionroles_database_filepath, database)

    @commands.command(aliases=["rrr"])
    @commands.has_permissions(manage_roles=True)
    async def removereactrole(self, ctx: commands.Context, role: discord.Role):
        """
        🏷️ Removes a reaction role message.

        Usage:
        ```
        ~removereactrole | ~rrr <@role>
        ```
        """

        data = self.client.cache.reactionroles
        instances = [item for item in data if item["role_id"] == role.id]
        if len(instances) == 0:
            raise commands.RoleNotFound(role.__str__())
        for instance in instances:
            msg = ctx.channel.get_partial_message(instance["msg_id"])
            await msg.delete()
            data.remove(instance)
        self.client.update_json(self.reactionroles_database_filepath, data)
        embed = discord.Embed(title="👍🏻 Done.", description=f"🔧 Removed '{role.name}'.")
        await ctx.send(embed=embed)

    @commands.command(alias=["roles"])
    async def viewreactroles(self, ctx: commands.Context):
        """
        🏷️ Shows all of the reaction roles in a server.

        Usage:
        ```
        ~removereactrole | ~rrr <@role>
        ```
        """
        roles = []
        db = self.client.cache.reactionroles

        for reaction_role_message in db:
            if reaction_role_message["guild_id"] != ctx.guild.id:
                continue

            role_id = int(reaction_role_message["role_id"])
            role = ctx.guild.get_role(role_id)

            roles.append(f"{role.name}")

        embed = discord.Embed(
            title=f"🏷️ Found {len(roles)} Reaction {'Roles' if len(roles) != 1 else 'Role'}",
            description=" ".join(f"`{role}`" for role in roles),
        )

        await ctx.send(embed=embed)

    @reactrole.error
    async def reactrole_error(self, ctx: commands.Context, error):
        """
        Error handler for the reactrole command.
        """
        error = getattr(error, "original", error)
        message = f"❌ "

        if isinstance(error, commands.RoleNotFound):
            message += "The role you specified was not found."

        if isinstance(error, commands.EmojiNotFound):
            message += "The emoji you specified was not found."

        if isinstance(error, commands.UserInputError):
            message += "Invalid input, please try again."

        if isinstance(error, commands.MissingRequiredArgument):
            message += "Please enter all the required arguments."

        if isinstance(error, discord.Forbidden):
            message += (
                "BB.Bot is forbidden from assigning/removing this role. "
                + "Try moving this role above the reaction role."
            )

        if (
            isinstance(error, discord.HTTPException)
            and "Unknown Emoji" in error.__str__()
        ):
            await ctx.channel.purge(limit=1)
            message += "Sorry, that emoji is invalid."

        await ctx.reply(message, delete_after=20)

    @removereactrole.error
    async def removereactrole_error(self, ctx: commands.Context, error):
        """
        Error handler for the removereactrole command.
        """
        error = getattr(error, "original", error)
        message = f"❌ "

        if isinstance(error, commands.RoleNotFound):
            message += "The role you specified was not found."

        if isinstance(error, commands.UserInputError):
            message += "Invalid input, please try again."

        if isinstance(error, commands.MissingRequiredArgument):
            message += "Please enter all the required arguments."

        await ctx.reply(message, delete_after=20)


async def setup(client: commands.Bot):
    """Registers the cog with the client."""
    await client.add_cog(RoleCog(client))


async def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    await client.remove_cog(RoleCog(client))
