"""
Contains a cog that handles reaction roles/self roles.
"""

import discord.ext.commands as commands
import discord
import helpers
import json

FILEPATH = 'files/reactionroles.json' # JSON file containing reaction role data


# |--- REACTION ROLES EVENT HANDLER ---|


class ReactionEventHandler(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        guild: discord.Guild = self.client.get_guild(payload.guild_id)

        if payload.member.bot: # If the user who added the reaction is the bot
            return

        with open(FILEPATH) as file:
            data: list = json.load(file)

            for item in data:
                if item['emoji'] != payload.emoji.name or item['msg_id'] != payload.message_id:
                    continue

                roles = guild.roles
                role = discord.utils.get(roles, id=item['role_id'])

                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        guild: discord.Guild = self.client.get_guild(payload.guild_id)
        member: discord.Member = guild.get_member(payload.user_id)

        if member.bot: # If the user who added the reaction is the bot
            return

        with open(FILEPATH) as file:
            data: list = json.load(file)

            for item in data:
                if item['emoji'] != payload.emoji.name or item['msg_id'] != payload.message_id:
                    continue

                roles = guild.roles
                role = discord.utils.get(roles, id=item['role_id'])

                await member.remove_roles(role)


# |---------- REACTION ROLES ----------|


@commands.command()
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx: commands.Context, emoji, role: discord.Role, *, message: str):
    """
    Creates and sends an embed that gives users a role when they react to it.
    """
    embed = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=embed)

    await msg.add_reaction(emoji)

    with open(FILEPATH) as file:
        data: list = json.load(file)

        react_role = {
            'name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'msg_id': msg.id
        }

        data.append(react_role)

    with open(FILEPATH, 'w') as file:
        json.dump(data, file, indent=4)


# |---- REGISTERING MODULE ----|


def setup(client: commands.Bot):
    """
    Registers the reaction roles cog with the bot.

    Parameters
    ----------

    client (Bot):
        The bot to add the commands to.
    """
    helpers.add_commands(client, reactrole)
    client.add_cog(ReactionEventHandler(client))