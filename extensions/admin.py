import discord
import asyncio
from discord.ext import commands


class Admin(commands.Cog):
    """Command category for administrator only commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", aliases=["b"], description="Bans a user from a server.")
    @commands.has_permissions(ban_members=True)
    async def ban_(self, ctx: commands.Context, user: discord.Member, *, reason=None):
        """Bans a user from a server.
        Requires the 'Ban members' permission.
        """

        if reason is None:
            await ctx.guild.ban(user, reason=reason)
            await user.send(f"📢 You have been banned in **{ctx.guild}**.")
        else:
            await ctx.guild.ban(user, reason=reason)
            await user.send(f"📢 You have been banned in **{ctx.guild}** for **{reason}**.")

        await ctx.send(f"✅ **{user.name}** has successfully been banned.")

    @commands.command(name="kick", aliases=["k"], description="Kicks a user from a server.")
    @commands.has_permissions(kick_members=True)
    async def kick_(self, ctx: commands.Context, user: discord.Member, *, reason=None):
        """Kicks a user from a server.
        Requires the 'Kick members' permission.
        """

        if reason is None:
            await user.kick()
            await user.send(f"📢 You have been kicked from **{ctx.guild}**.")
        else:
            await user.kick(reason=reason)
            await user.send(f"📢 You have been kicked from **{ctx.guild}** for **{reason}**.")

        await ctx.send(f"✅ {user.name} has successfully been kicked.")

    @commands.command(name="restrict", aliases=["rs"],
                      description="Assigns a role 'Restricted' to a user."
                                + "This role must be added and configured by hand.")
    @commands.has_permissions(manage_roles=True)
    async def restrict_(self, ctx: commands.Context, member: discord.Member, duration_in_seconds: int):
        """Gives a role 'Restrict' to the user for X seconds.
        1. The role MUST already exist on the server it's used on.
        2. The role permissions must be configured by hand.
        """

        try:
            role = discord.utils.get(ctx.guild.roles, name="Restricted")
            duration_in_milliseconds = duration_in_seconds * 1000

            await member.add_roles(role)
            await asyncio.sleep(duration_in_milliseconds)
            await member.remove_roles(role)
        except:
            await ctx.send("❌ You don't have a 'Restricted' role. Please create one to use this command.")
            return


def setup(bot: commands.Bot):
    """Adds the Admin cog to the bot."""
    bot.add_cog(Admin(bot))